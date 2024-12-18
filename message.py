# 今日の更新
# Copyright (C) 2024 FUJITSU LIMITED
#
import logging


class LoggerConfig:
    @staticmethod
    def configure_logging():
        logger = logging.getLogger()
        # ログレベルをINFOに設定, INFOレベル以上を出力

        # INFOメッセージ用のフォーマッタ
        info_formatter = logging.Formatter(
            "[Info] %(asctime)s, %(message)s", datefmt="%Y/%m/%d %H:%M:%S"
        )

        # コンソールにメッセージを表示するため、StreamHandlerを使用
        info_handler = logging.StreamHandler()
        # INFOメッセージ用のフォーマッタを設定
        info_handler.setFormatter(info_formatter)
        logger.setLevel(logging.INFO)
        info_handler.addFilter(lambda record: record.levelno < logging.ERROR)
        # ハンドラーに追加　？
        logger.addHandler(info_handler)

        # ERRORメッセージ用のフォーマッタ
        error_formatter = logging.Formatter(
            "[Error] %(asctime)s, %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )

        error_handler = logging.StreamHandler()
        error_handler.setFormatter(error_formatter)
        # ログレベルをERRORに設定, ERRORレベル以上を出力
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)
