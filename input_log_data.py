#
# Copyright (C) 2024 FUJITSU LIMITED
#
import os
import logging


class InputLogData:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.log_file = ""
        self.lines = []

    # .logファイルの存在を確認
    def list_files(self) -> bool:
        # TODO 戻り値の型を明示的に
        files = os.listdir(self.folder_path)
        # dataフォルダ内の.logファイルの存在をチェック
        log_files = [f for f in files if f.endswith(".log")]
        if len(log_files) != 1:
            error_message = f"UERR002, {self.folder_path} 配下に.logの拡張子のついたファイルが無い、または複数あります"
            logging.error(error_message)
            return False
        else:
            self.log_file = log_files[0]
            return True
            # self.file_name = os.path.join(self.folder_path, self.log_file)

    # 存在確認したファイルを読み込む
    def read_lines(self) -> bool:
        # TODO log_fileが空文字だとエラーにする
        # open関数にて.logファイルを開き、全行をfに格納
        # TODO file_pathがブランクのかのうせいもあるよね、どう処理するか
        file_path = os.path.join(self.folder_path, self.log_file)
        with open(file_path, "r", encoding="utf-8") as f:
            # .logファイルの中身を全行読みこんだものをリストに追加
            # self.lines = f.readlines()
            self.lines = [line.split(",")[2].strip('"') for line in f.readlines()]

        # ファイルが空の場合にエラーを出す
        if len(self.lines) == 0:  # TODO ブランクスペースは通る？ 通った、、、。
            error_message = f"UERR003,{self.log_file}が空です"
            logging.error(error_message)
            return False

        return True
