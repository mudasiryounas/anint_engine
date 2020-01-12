# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from core import db_session
from core.db_models import AppsToFollow

TOPSELLING_NEW_FREE_URL = 'https://play.google.com/store/apps/collection/topselling_new_free?gl={}&hl={}'

def check_for_new_released_apps():
    print("check for new released apps job started")
    country_lang_pairs_to_check = [('us', 'en'), ('us', 'tr'), ('tr', 'en'), ('tr', 'tr')]
    extracted_ids = set()
    for country, lang in country_lang_pairs_to_check:
        url = TOPSELLING_NEW_FREE_URL.format(country, lang)
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf8')
        app_hrefs = soup.select('[href^="/store/apps/details?id="]')
        for item in app_hrefs:
            app_id = item.attrs['href'].split('id=')[-1]
            extracted_ids.add(app_id)
    if extracted_ids:
        print(f"Total '{len(extracted_ids)}' ids extracted...")
        for package in extracted_ids:
            app_to_follow = db_session.query(AppsToFollow).filter_by(package=package).first()
            if app_to_follow is None:
                app_to_follow = AppsToFollow(package=package, insert_date=datetime.utcnow())
                db_session.add(app_to_follow)
        db_session.commit()
    print("check for new released apps job finished")


if __name__ == '__main__':
    check_for_new_released_apps()
