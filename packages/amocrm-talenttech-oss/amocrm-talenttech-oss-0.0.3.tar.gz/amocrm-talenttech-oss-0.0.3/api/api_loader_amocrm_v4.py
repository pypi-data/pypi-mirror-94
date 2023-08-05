import sys
import requests
import json
import logging
from datetime import datetime, timedelta
from s3.client import Client

PAGE_NUMBER_MAX = 1e6


def process_json(data, entity):
    """
    update data after retrieving from s3
    Args:
        data: row data json
    Returns: list
    """
    return data["_embedded"][entity]


class AmocrmApiLoader:
    """
    CLASS API LOADER to S3 Directory
    """

    def __init__(
            self,
            entity,
            s3_path,
            s3_token_path,
            args_s3,
            args_api,
            date_modified_from=None,
            with_offset=True,
            batch_api=250,
    ):
        """
        :param entity:   amocrm entities contacts/users/accounts e.t.c
        :param s3_path:  path where is files should be uploaded
        :param s3_token_path:  s3 path where is saved last token
        :param args_s3:  dict with aws_access_key_id/aws_secret_access_key/endpoint_url/bucket
        :param args_api: dict with AMO_USER_LOGIN/AMO_USER_HASH/AMO_AUTH_URL
        :param date_modified_from:
        :param with_offset:
        :param batch_api: size of batch to upload
        """
        log_format = "%(asctime)-15s %(name)s:%(levelname)s: %(message)s"
        logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)
        logging.basicConfig(format=log_format, stream=sys.stderr, level=logging.ERROR)
        logging.captureWarnings(True)
        self.logger = logging.getLogger(__class__.__name__)

        self.entity = entity

        self.args_api = args_api
        self.batch_api = batch_api
        self.date_modified_from = date_modified_from
        self.with_offset = with_offset

        self.s3_token_path = s3_token_path
        self.s3_path = s3_path
        self.s3_client = Client(**args_s3)

        self.access_token = None
        self.rows_to_upload = 0

    def __save_tokens_s3(self, data):
        """
        Save data with tokens to s3
        :return:None
        """
        expires_in_datetime = datetime.now() + timedelta(seconds=data["expires_in"])
        data["expires_in_datetime"] = expires_in_datetime.strftime("%Y-%m-%d %H:%M")
        self.logger.info("Modifying config {}...".format(self.s3_token_path))
        self.s3_client.create_file(self.s3_token_path, json.dumps(data))
        self.logger.info(
            "Save new refresh and access token to...".format(self.s3_token_path)
        )

    def __get_tokens(self, args):
        """
        Get tokens and additional params
        :param args: dict with code or refresh_token
        :return: dict with refresh and access token
        """
        data = {
            "client_secret": self.args_api["CLIENT_SECRET"],
            "client_id": self.args_api["CLIENT_ID"],
            "redirect_uri": self.args_api["REDIRECT_URL"],
        }
        data.update(args)
        resp = requests.post(self.args_api["AUTH_URL"], data=data).json()
        if "refresh_token" not in resp and "access_token" not in resp:
            raise Exception(
                "An error occurred while retrieving auth params: " + str(resp)
            )
        else:
            return resp

    def auth(self, code_auth=None):
        """API authorization auth2"""
        # read file from s3 if exists
        try:
            self.logger.info(
                "Load refresh and access token from file {}".format(self.s3_token_path)
            )
            response = json.loads(self.s3_client.read_file(self.s3_token_path))
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            if (
                    now_str < response["expires_in_datetime"]
            ):  # check if access token is still valid
                self.access_token = response["access_token"]
                return True
            else:
                response = self.__get_tokens(
                    args={
                        "refresh_token": response["refresh_token"],
                        "grant_type": "refresh_token",
                    }
                )
        except:
            self.logger.warning(
                "If you got here you should to regenerate refresh token"
            )
            if code_auth is None:
                raise NotImplementedError(
                    "You should pass code_auth argument to save the new refresh and access tokens (or get and save "
                    "them the first time) "
                )
            response = self.__get_tokens(
                args={"code": code_auth, "grant_type": "authorization_code"}
            )

        self.access_token = response["access_token"]
        self.__save_tokens_s3(response)

    def get_headers(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token,
        }
        return headers

    def clear_s3_folder(self):
        if self.s3_client.path_exists(self.s3_path):
            for file in self.s3_client.get_file_list(self.s3_path):
                self.logger.info("Delete {file} from s3".format(file=file))
                self.s3_client.delete_file(path=file)
            self.s3_client.delete_dir(self.s3_path)  # remove directory

    def __get_file_name(self, offset, batch):
        """
        Returns: s3 file name
        """
        return "{dir_path}/{entity}_{offset}_{batch}.json".format(
            dir_path=self.s3_path, entity=self.entity, offset=offset, batch=batch
        )

    def extract(self):
        """load table from api"""
        self.auth()
        if not self.s3_client.path_exists(self.s3_path):
            self.s3_client.create_dir(self.s3_path)
        self.clear_s3_folder()  # clear old before loading

        url_base = self.args_api["amocrm_api_url"]
        cur_page = 1
        count_uploaded = self.batch_api

        params = {}
        if self.date_modified_from is not None:
            self.logger.info("Uploading data with after {}".format(self.date_modified_from))
            params["filter[updated_at][from]"] = int(
                self.date_modified_from.timestamp()
            )

        while cur_page < PAGE_NUMBER_MAX and count_uploaded == self.batch_api:
            self.logger.info("Extracting page number {}".format(cur_page))
            file_path = self.__get_file_name(cur_page, self.batch_api)

            if self.with_offset == 1:
                url = url_base.format(limit=self.batch_api, page=cur_page)
            else:
                url = url_base

            self.logger.info(url)
            objects = requests.get(url, headers=self.get_headers(), params=params)
            if objects.status_code == 204:
                self.logger.warning("Warning! API sent no result {}".format(objects.status_code))
                return

            count_uploaded = len(process_json(objects.json(), self.entity))
            self.rows_to_upload += count_uploaded
            self.logger.info(
                "Saving data in file {}, count rows {}, total: {}".format(
                    file_path, count_uploaded, self.rows_to_upload
                )
            )
            self.s3_client.create_file(file_path, objects.content)

            cur_page += 1
        self.logger.info("Total number of rows received from API is {}".format(self.rows_to_upload))
