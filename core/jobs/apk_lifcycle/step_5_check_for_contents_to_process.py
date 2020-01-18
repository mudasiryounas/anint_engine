# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import time
from datetime import datetime

from ioc_finder import find_iocs

from core import db_session
from core.Enums import ContentStatus
from core.db_models import AppContents
from core.utils.domain_utils import DomainUtils
from core.utils.ip_utils import IpUtils
from core.utils.phonenumber_utils import PhoneNumberUtils
from core.utils.url_utils import UrlUtils
from core.utils.tools import Tools


def main():
    unprocessed_contents = db_session.query(AppContents).filter_by(content_status=ContentStatus.UNPROCESSED.value).limit(100).all()
    print(f"Total '{len(unprocessed_contents)}' unprocessed contents will be processed...")
    for item in unprocessed_contents:
        start_time = time.time()
        content = item.content
        app_id = item.app_id
        iocs = find_iocs(content)

        IpUtils.save_ipv4s(app_id, iocs.get('ipv4s'))
        IpUtils.save_ipv6s(app_id, iocs.get('ipv6s'))
        IpUtils.save_ipblocks(app_id, iocs.get('ipv4_cidrs'))
        DomainUtils.save_domains(app_id, iocs.get('domains'))
        UrlUtils.save_urls(app_id, iocs.get('urls'))
        PhoneNumberUtils.save(app_id, iocs.get('phone_numbers'))

        item.content_status = ContentStatus.PROCESSED.value
        item.update_date = datetime.utcnow()
        db_session.commit()
        print(f"processing for app_id: '{item.app_id}', file: '{item.content_file}' finished, Took '{Tools.get_elapsed_time(start_time)}' seconds")


if __name__ == '__main__':
    main()
