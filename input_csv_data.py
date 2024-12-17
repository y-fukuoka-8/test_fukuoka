#
# Copyright (C) 2024 FUJITSU LIMITED
#
import os
import csv
import logging


class InputCSVData:
    def __init__(self, folder_path: str):
        # フォルダのパスをインスタンス変数に格納
        self.folder_path = folder_path
        # .csvファイルのリストを格納するインスタンス変数を初期化
        self.csv_files = []
        # .csvファイルの全行を格納するインスタンス変数を初期化
        self.all_rows = []

    def list_files(self) -> bool:
        # フォルダ内のファイルをリスト化
        files = os.listdir(self.folder_path)
        # .csvファイルの存在をチェック（result.csvファイルは除外する）
        csv_files = [f for f in files if f.endswith(".csv") and f != "result.csv"]
        # .csvファイルが存在しない場合はエラーを出す
        if len(csv_files) == 0:
            error_message = f"UERR001, {self.folder_path} 配下に.csvの拡張子のついたファイルがありません"
            logging.error(error_message)
            return False
        # 戻り値は設定せず、インスタンス変数に格納し、自身で保持する
        else:
            self.csv_files = csv_files
            return True
        #    return [os.path.join(self.folder_path, f) for f in csv_files]

    def read_csv_files(self) -> bool:
        # 存在確認したファイルを読み込む
        for file_name in self.csv_files:
            file_path = os.path.join(self.folder_path, file_name)
            # utf-8-sigにした理由
            # 空のcsvファイルを読み込むと、なぜか[ufeff]がリストに入る
            # バイト順マーク、通称BOMと呼ばれる特殊文字列が入る
            # 　ufeffはユニコード文字U+FEFFを表し、不可視文字である
            # utf-8-sigで読み込むことで、BOMを取り除くことができる
            # https://qiita.com/Ryo-0131/items/7d6b1c772b32c3bbe15e
            with open(file_path, "r", encoding="utf-8-sig") as f:
                # csv.readerでファイルを読み込む
                reader = csv.reader(f)
                self.rows = list(reader)

                # ファイルが空の場合にエラーを出す
                if len(self.rows) == 0:
                    error_message = f"UERR003,{file_name}が空です"
                    logging.error(error_message)
                    return False
                else:
                    self.all_rows.extend(self.rows)

        return True
