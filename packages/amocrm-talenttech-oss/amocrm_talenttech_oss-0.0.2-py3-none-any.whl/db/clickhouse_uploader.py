import logging
import sys
import json
from s3.client import Client as S3Client
from api.api_loader_amocrm_v4 import process_json

from clickhouse_balanced import Client
import pandas as pd

from converter.fields_converter_oneway import FieldsConverterOneWay


class UploaderDB:
    def __init__(
            self,
            args_s3,
            s3_path,
            sql_credentials,
            entity,
            table_name,
            table_to_optimize=None,
            files_in_upload=5,
            full_copy=False,
            json_columns=None
    ):
        """
        Class to put the data from s3 into vertica
        :param args_s3:  s3 variable dict
        :param s3_path:
        :param sql_credentials clickhouse variable dict
        :param entity:
        :param table_name:
        :param table_to_optimize: in a few cases
        :param files_in_upload: a number of files in upload
        :param full_copy: if True will make truncate and insert
        :param json_columns: list of columns need to beatify as json
        """
        log_format = "%(asctime)-15s %(name)s:%(levelname)s: %(message)s"
        logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)
        logging.basicConfig(format=log_format, stream=sys.stderr, level=logging.ERROR)
        logging.captureWarnings(True)
        self.logger = logging.getLogger(__class__.__name__)

        self.files_in_upload = files_in_upload
        self.sql_credentials = sql_credentials

        self.s3_path = s3_path
        self.s3_client = S3Client(**args_s3)

        self.uploaded_rows = 0
        self.table_name = table_name
        self.table_to_optimize = table_to_optimize
        self.full_copy = full_copy
        self.json_columns = json_columns or []

        self.entity = entity
        self.columns = None

    def __update_data(self, data, table_name):
        """
        Date transformation for further update
        :param data:
        :param table_name:
        :return: transformed data
        """
        df = pd.DataFrame(data=data).drop_duplicates(subset=["id"])
        df_updated = df.where(pd.notnull(df), None).dropna(how="all", axis=1)
        for column in self.json_columns:
            if column in df_updated.columns:
                df_updated[column] = df_updated.apply(
                    lambda x: json.dumps(x[column], ensure_ascii=False)
                    if x[column] is not None
                    else None,
                    axis=1,
                )
        converter = FieldsConverterOneWay(sql_credentials=None, db="ch")
        items = converter.update_value_type(
            table_name=table_name,
            items=df_updated.to_dict(orient="records"),
            fields=self.columns,
        )
        del df, df_updated, converter
        return items

    def __get_columns(self, table_name, ch_client):
        column_stat = """select name, type
            from  system.columns
            where table = '{table}'
                  and database = '{database}'
                  """.format(
            table=table_name, database=self.sql_credentials["database"]
        )
        rows = ch_client.execute(column_stat)
        res = dict(zip([row[0] for row in rows], [row[1] for row in rows]))
        return res

    def __delete_from_db(self, table_name, ch_client, to_delete_values=[], delete_column="id"):
        """
        To delete already existed items from table
        Args:
            table_name:
            to_delete_values:  ids of deleted values
            delete_column: fields of ids

        Returns: Nothing
        """
        logging.info(
            "Deleting custom fields from {table}, for {count} leads".format(
                table=table_name, count=len(to_delete_values)
            )
        )

        columns = self.__get_columns(table_name)
        columns_str = ",".join(columns)
        columns_changed_str = ",".join(
            ["-1" if c == "sign" else str(c) for c in columns]
        )

        if "sign" not in columns:
            logging.info("No sign for deleting in columns")
            return

        index = 0
        len_update = 1000
        row_deleted_count = len(to_delete_values)
        while index < len(to_delete_values):
            cur_deleted_values = ",".join(
                [str(r) for r in to_delete_values[index: index + len_update]]
            )
            select_st = f"select {columns_changed_str} from {table_name} where sign = 1 and {delete_column} in ({cur_deleted_values})"
            insert_st = f"insert into {table_name} ({columns_str}) {select_st} "
            ch_client.execute(insert_st)
            index += len_update

        logging.info(
            "Deleting custom fields from {table} success, {count} deleted leads".format(
                table=table_name, count=row_deleted_count
            )
        )

    def __upload_data_to_db(self, data, ch_client, table_name=None):
        """
        Row uploading data to table
        Args:
            data:
            table_name:
        Returns: Nothing
        """
        table_name = table_name or self.table_name
        columns = ",".join([c for c in self.columns if c in data[0].keys()])
        logging.info("Insert values to {} count {}".format(table_name, len(data)))
        logging.info(f"INSERT INTO {table_name} ({columns}) VALUES")
        ch_client.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES", data, types_check=True
        )

    def __optimize_table_ch(self, table, ch_client, add=""):
        """optimize table, set only for clickhouse"""
        sql_cf_optimize = (
            "Optimize table {database}.{table}  {add} ".format(
                database=self.sql_credentials["database"],
                table=table,
                add=add,
                cluster="{cluster}",
            )
        )
        logging.info(sql_cf_optimize)
        ch_client.execute(sql_cf_optimize)

    def __generate_table_ddl(self, file_path):
        """
        Get approximate table ddl
        :param file_path:
        :return: approximate dll of the table you need to create
        """
        converter = FieldsConverterOneWay(sql_credentials=None, db="ch")
        cur_data = process_json(
            json.loads(self.s3_client.read_file(file_path)), self.entity
        )
        return converter.create_table_from_dataframe(
            dataframe=pd.DataFrame(data=cur_data),
            table_name=self.table_name,
            to_create=False,
            schema=self.sql_credentials["database"],
        )

    def __log_status(self, cty_upload):
        logging.info(
            "Loading {} rows to {} is successful, cum:{}".format(
                cty_upload,
                self.table_name,
                self.uploaded_rows,
            )
        )

    def load_s3_to_db(self):
        ch_client = Client(**self.sql_credentials)
        cur_file = 1
        data = []
        paths = self.s3_client.get_file_list(self.s3_path)
        total_files = len(paths)
        self.columns = self.__get_columns(self.table_name, ch_client)
        if len(self.columns) == 0:
            self.logger.error(
                "You should create table {}.{}".format(
                    self.sql_credentials["database"], self.table_name
                )
            )
            if total_files > 0:
                self.logger.info("You can try to create table like that " + self.__generate_table_ddl(paths[0]))
            raise ModuleNotFoundError('Table not found exception')

        if self.full_copy:
            sql_truncate = f"truncate table {self.table_name}"
            logging.info(sql_truncate)
            ch_client.execute(sql_truncate)

        for file_path in paths:
            self.logger.info("Loading data from the file %s" % file_path)

            cur_data = process_json(
                json.loads(self.s3_client.read_file(file_path)), self.entity
            )
            data += cur_data
            if cur_file % self.files_in_upload == 0 or cur_file == total_files:
                data = self.__update_data(data=data, table_name=self.table_name)
                self.__upload_data_to_db(data=data, ch_client=ch_client)
                self.uploaded_rows += len(data)
                self.__log_status(cty_upload=len(data))
                data = []
            cur_file += 1

        if self.table_to_optimize is not None:
            self.__optimize_table_ch(table=self.table_to_optimize, ch_client=ch_client)
