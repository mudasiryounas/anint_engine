# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from core import db_session
from core.db_models import AppsToFollow
from datetime import datetime


class AppsToFollowUtils:
    @staticmethod
    def update(package, status, new_version):
        app_to_follow = db_session.query(AppsToFollow).filter_by(package=package).first()
        app_to_follow.status = status
        app_to_follow.last_version = app_to_follow.current_version
        app_to_follow.current_version = new_version
        app_to_follow.update_date = datetime.utcnow()
        db_session.commit()
