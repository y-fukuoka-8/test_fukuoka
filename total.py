#
# Copyright (C) 2024 FUJITSU LIMITED
#
from data_mng import DataMng


def main():
    # フォルダのパスと出力ファイル名を指定
    folder_path = "data"
    output_file = "result.csv"

    # DataMngクラスのインスタンスを作成し、DataMngクラスのprocessメソッド実行
    data_mng = DataMng(
        folder_path,
        output_file,
    )
    data_mng.process()


# スクリプトの実行
if __name__ == "__main__":
    main()
