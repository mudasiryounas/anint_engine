# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from datetime import datetime

from core import db_session
from core.db_models import Urls


class UrlUtils:
    @staticmethod
    def save(app_id, url_list):
        for url in url_list:
            url_entity = Urls(app_id=app_id,
                              url=url,
                              insert_date=datetime.utcnow(),
                              update_date=datetime.utcnow())
            db_session.add(url_entity)
        db_session.commit()
