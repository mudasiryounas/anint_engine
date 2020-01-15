# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from core import db_session
from core.Enums import ContentStatus
from core.db_models import AppContents
from ioc_finder import find_iocs

from core.utils.domain_utils import DomainUtils
from core.utils.ip_utils import IpUtils
from core.utils.phonenumber_utils import PhoneNumberUtils
from core.utils.url_utils import UrlUtils
from datetime import datetime


def main():
    unprocessed_contents = db_session.query(AppContents).filter_by(content_status=ContentStatus.UNPROCESSED.value).limit(500).all()
    for item in unprocessed_contents:
        content = item.content
        app_id = item.app_id
        iocs = find_iocs(content)

        IpUtils.save_ipv4s(app_id, iocs.get('ipv4s'))
        IpUtils.save_ipv6s(app_id, iocs.get('ipv6s'))
        IpUtils.save_ipblocks(app_id, iocs.get('ipv4_cidrs'))
        DomainUtils.save(app_id, iocs.get('domains'))
        UrlUtils.save(app_id, iocs.get('urls'))
        PhoneNumberUtils.save(app_id, iocs.get('phone_numbers'))

        item.status = ContentStatus.PROCESSED.value
        item.update_date = datetime.utcnow()
        db_session.commit()


if __name__ == '__main__':
    main()
