# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import play_scraper


class PlaystoreUtils:
    @staticmethod
    def get_app_latest_info(package):
        app = play_scraper.details(package)
        return app


