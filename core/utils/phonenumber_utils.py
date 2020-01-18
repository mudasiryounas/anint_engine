# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from datetime import datetime

from core import db_session
from core.db_models import PhoneNumbers


class PhoneNumberUtils:
    @staticmethod
    def save(app_id, phone_number_list):
        for phone_number in phone_number_list:
            phone_number_entity = db_session.query(PhoneNumbers).filter_by(app_id=app_id).filter_by(phone_number=phone_number).first()
            if phone_number_entity is None:
                phone_number_entity = PhoneNumbers(app_id=app_id,
                                                   phone_number=phone_number,
                                                   insert_date=datetime.utcnow(),
                                                   update_date=datetime.utcnow())
                db_session.add(phone_number_entity)
        db_session.commit()
