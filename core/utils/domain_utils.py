# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from datetime import datetime

from core import db_session
from core.db_models import Domains


class DomainUtils:
    @staticmethod
    def save(app_id, domain_list):
        for domain in domain_list:
            domain_entity = Domains(app_id=app_id,
                                    domain=domain,
                                    insert_date=datetime.utcnow(),
                                    update_date=datetime.utcnow())
            db_session.add(domain_entity)
        db_session.commit()
