# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from core import db_session
from core.Enums import ContentStatus
from core.db_models import AppContents


def main():
    unprocessed_contents = db_session.query(AppContents).filter_by(content_status=ContentStatus.UNPROCESSED.value).limit(500).all()
    for item in unprocessed_contents:
        pass # process for IOC and insert into ips emails etc


if __name__ == '__main__':
    main()
