# コミットを理解するためのコメント
# Copyright (C) 2024 FUJITSU LIMITED
#
import csv
import re
from collections import defaultdict
import logging


class OutputCSVData:
    def __init__(self, output_file: str):
        self.output_file = output_file
        # defaultdictを使うことで、キーが存在しない場合にあらかじめ指定したリストを返す（Keyエラーを防ぐ）
        self.extracted_info = defaultdict(lambda: ["", "", "", ""])

    def extract_from_syslog(self, lines, pr_name_map) -> bool:
        # .logファイルの中身を1行ずつ読み込み、正規表現で情報を抽出
        for line_number, line in enumerate(lines, start=1):
            # message = line.split(",")[2].strip('"')
            # print(message)
            room_match = None
            start_index = line.find("TOP/")
            if start_index != -1:
                # TOP/の長さは4文字なので、TOP/" の直後から切り出すために+4をする
                room_match = line[start_index + 4 : line.rfind("(")].strip()

            # room_matchに正規表現で抽出した値を格納
            # TOP/から(までの文字列を抽出 [^()]+は()以外の文字列を表す
            # ()でグループ化を行う　group(0)は完全一致部分抽出、group(1)は()内の部分抽出
            # room_match = re.search(r"TOP/([^(]+)\(", line)

            # 2 room_match = re.search(r"TOP/([^()]+(?:\([^(]*\))?\d+)", line)
            # 3room_match = re.search(r"TOP/([^()]+(?:\([^()]*\))?[^()]*\d+)", line)

            # Project: Domain:で条件を指定し、その中の()内の数字を抽出
            # (\d+)は1文字以上の数字を表す
            # ()内の文字列を抽出するために"."と"*"を使う
            # "."は任意の1文字、"*"は0回以上の繰り返しを表す
            # よって、".*"は任意の文字列が0回以上繰り返されることを表す
            project_match = re.search(r"Project: Domain:.*\((.*)\)", line)
            # Project Task: Domain:で条件を指定し、その中の()内の数字を抽出
            task_match = re.search(r"Project Task: Domain:.*\((.*)\)", line)

            # TODO:15～17行目の説明（正規表現の理解をするだけで価値あり）

            # romm_matchに格納された値が空文字列でないかを判定 空文字ならばFalse, 空文字でなければTrueが返される
            if room_match is not None:  # TODO: 論理式で！！！
                # room_matchに格納された値(group(1)で部分一致)をroom_nameに格納
                room_name = (
                    room_match  # .group(1)  #TODO:グループの言語仕様について調べる
                )
                pr_id = ""
                # TODO: mapについてサンプルコードで動作確認する

                # pr_name_map辞書からpr_nameをキーにしてpr_idを取得
                for pr_name in pr_name_map:
                    # room_name + "_SNB"がpr_nameに含まれている場合、pr_idにpr_name_mapの値を格納
                    if room_name + "_SNB" in pr_name:
                        pr_id = pr_name_map[pr_name]

                # project_matchに格納された値が空文字列でないかを判定 空文字ならばFalse, 空文字でなければTrueが返される
                if project_match is not None:
                    # project_matchに格納された値(group(1)で部分一致)をproject_str_orgに格納
                    project_str_org = project_match.group(1)  # TODO: 同上
                    # 抽出した"project_str_org"をextracted_infoの3列目に格納
                    # self.extracted_info[room_name][2] = project_str_org

                    # 数値に変換出来るかの判定
                    if project_str_org.isdigit():
                        self.extracted_info[room_name][2] = project_str_org
                    else:
                        error_message = f"UERR004, ログファイル内のTOP/XXXXXXA()の()内が何も書かれていないor数字以外が入っています\n ログファイルの{line_number}行目"
                        logging.error(error_message)
                        return False
                    # 間を埋める

                # task_matchに格納された値が空文字列でないかを判定 空文字ならばFalse, 空文字でなければTrueが返される
                if task_match is not None:
                    # task_matchに格納された値(group(1)で部分一致)をtask_countに格納
                    task_count = task_match.group(1)
                    # 抽出した"task_count"をextracted_infoの4列目に格納
                    if task_count.isdigit():
                        self.extracted_info[room_name][3] = task_count
                    else:
                        error_message = f"UERR004, ログファイル内のTOP/XXXXXXA()の()内が何も書かれていないor数字以外が入っています\n ログファイルの{line_number}行目"
                        logging.error(error_message)
                        return False
                    # 抽出した"pr_id"と"room_name"をextracted_infoの1,2列目に格納

                self.extracted_info[room_name][0] = pr_id
                self.extracted_info[room_name][1] = room_name

        return True

    def extract_from_pjroom(self, rows) -> dict:
        # 空の辞書"pr_name_map"を初期化
        pr_name_map = {}
        # ヘッダー行を取得
        header = rows[0]
        # ヘッダー行からPR_nameとIDのインデックスを取得
        # 列指定しないことで、順番が変わっても対応できる（最初は列指定してた、。）
        # 要件定義書にて、列の順番が変わる可能性があると記載されていた
        if "PR_name" in header:
            pr_name_index = header.index("PR_name")
        else:
            error_message = (
                f'UERR007, CSVファイル内のヘッダー行に "PR_name" が存在しません'
            )
            logging.error(error_message)
            return None

        if "ID" in header:
            pr_id_index = header.index("ID")
        else:
            error_message = f'UERR008, CSVファイル内のヘッダー行に "ID" が存在しません'
            logging.error(error_message)
            return None

        # service_used#Idのインデックスを取得
        if "service_used#Id" in header:
            service_used_id_index = header.index("service_used#Id")
        else:
            error_message = (
                f'UERR009, CSVファイル内のヘッダー行に "service_used#Id" が存在しません'
            )
            logging.error(error_message)
            return None

        #  ヘッダー行をスキップしたいため、[1:]で2行目以降を取得
        # 行番号を取得するためにenumerateを使用
        # スタートカウントはstart=2を指定（2行目からカウントしたいから）
        for line_number, row in enumerate(rows[1:], start=2):

            # PR_nameとIDを取得
            pr_name = row[pr_name_index]
            pr_id = row[pr_id_index]
            service_used_id = row[service_used_id_index]

            # service_used#Idの値を取得
            # []を削除するためにre.subを使用
            # 正規表現パターンで[]を指定する
            # []を削除するために、第二引数で空文字を指定
            service_used_id_org = re.sub(r"[\[\]]", "", service_used_id)

            if service_used_id_org == "service_used#Id":
                continue

            # service_used#Idの値が数字かどうかを判定
            if service_used_id_org.isdigit():
                # 配列を文字列で格納
                pr_name_map[pr_name] = pr_id
            else:
                print(service_used_id_org)
                error_message = f"UERR006, service_used#Idの値が数字以外または空白です\n {line_number}行目"
                logging.error(error_message)
                return None
        return pr_name_map

    def write(self) -> None:
        # 余分な空行を削除するためにnewline=""を指定
        with open(self.output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            # ヘッダー行を書き込む
            writer.writerow(
                [
                    "ルームID",
                    "ルーム名称",
                    "プロジェクトの登録レコード数",
                    "タスクの登録レコード数",
                ]
            )
            # extracted_infoの値を書き込む
            for counts in self.extracted_info.values():
                if counts[2] == "":
                    counts[2] = 0
                if counts[3] == "":
                    counts[3] = 0
                writer.writerow(counts)
