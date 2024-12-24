# 　カリスマ
# Copyright (C) 2024 FUJITSU LIMITED
# 12/20
# いつになればコンフリクト起こりますか
from input_csv_data import InputCSVData
from input_log_data import InputLogData
from output_csv_data import OutputCSVData
import os
import logging
from message import LoggerConfig
import time


LoggerConfig.configure_logging()


class DataMng:
    # フォルダのパスと出力ファイル名を指定
    def __init__(self, folder_path, output_file):
        print("Ver.1.0.2")
        if not os.path.exists(folder_path):
            logging.error(f"UERR010, dataフォルダが存在しません")
            self.initialized = False

        else:
            self.csv_loader = InputCSVData(folder_path)
            self.log_loader = InputLogData(folder_path)
            self.csv_output = OutputCSVData(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), output_file)
            )
            self.initialized = True

        # 17行目～の説明
        # ハードコーディングではなく、ファイルの絶対パスを取得するためにos.path.dirname(os.path.abspath(__file__))を使用

    def process(self) -> None:
        if not self.initialized:
            return

        start_time = time.time()
        logging.info("INFO001, 処理を開始します")
        # .csvファイルの存在を確認
        if self.csv_loader.list_files() == False:
            return
        # .logファイルの存在を確認
        if self.log_loader.list_files() == False:
            return
        # csvファイルの中身を全行読み込む
        if self.csv_loader.read_csv_files() == False:
            return
        # .logファイルを読み込み、全行の情報を抽出
        if self.log_loader.read_lines() == False:
            return

            # "PR_name"と"ID"の情報を抽出し、pr_name_mapに格納
        pr_name_map = self.csv_output.extract_from_pjroom(self.csv_loader.all_rows)
        # extract_from_pjroomメソッドの戻り値がbool型ではないため、Noneで判定
        if pr_name_map == None:
            return
        # 全行の情報を抽出したものをcsv_outputのextract_from_syslogメソッドに渡し、正規表現で情報を抽出
        if (
            self.csv_output.extract_from_syslog(self.log_loader.lines, pr_name_map)
            == False
        ):
            return
        # 抽出した情報をCSVファイルに書き込む
        self.csv_output.write()

        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info("INFO002, 処理が終了しました")
        print(f"処理時間:{elapsed_time:.2f}秒")

        return
