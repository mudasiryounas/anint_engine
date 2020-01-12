# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import time

from core import db_session
from core.Enums import AppsToFollowStatus
from core.db_models import AppsToFollow
from core.utils.app_utils import AppUtils
from core.utils.apps_to_follow_utils import AppsToFollowUtils
from core.utils.playstore_utils import PlaystoreUtils


def check_for_all_app_updates():
    apps_to_follow = db_session.query(AppsToFollow).all()
    apps_to_follow_packages = [item.package for item in apps_to_follow]
    print(f"Adding '{len(apps_to_follow_packages)}' apps to queue for checking updates")
    for package in apps_to_follow_packages:
        check_for_app_updates(package)


def check_for_app_updates(package):
    start_time = time.time()
    print(f"Check for update job started for app: '{package}'")
    current_app_on_db = AppUtils.get_app(package)
    new_version = None
    if current_app_on_db is None:
        print(f"Check for update job is running first time for app: '{package}'")
        added_app = AppUtils.add_new_app(package)
        new_version = added_app.current_version
    else:
        # check if application version is updated from playstore
        latest_playstore_app = PlaystoreUtils.get_app_latest_info(package)
        if current_app_on_db.current_version != latest_playstore_app['current_version']:
            # if application version is updated, process latest apk
            print(f"New version is detected for app: '{package}', new version: '{latest_playstore_app['current_version']}' old version: '{current_app_on_db.current_version}'")
            new_version = latest_playstore_app['current_version']
        # update application details on db, even if version is not updated, in order to keep application details history
        AppUtils.update_app(package, latest_playstore_app)

    if new_version:
        print(f"Following app will be downloaded, decompiled and processed, app: '{package}', version: '{new_version}'")
        # todo automate downloading process
        # download latest apk
        # decompile latest apk
        # process latest decompiled files
        AppsToFollowUtils.update(package=package, status=AppsToFollowStatus.NEW_VERSION_DETECTED.value, new_version=new_version)
    else:
        print(f"No new version is detected for app: '{package}'")
    print(f"Check for update job finished for app: '{package}', Took '{round((time.time() - start_time), 4)}' seconds")


if __name__ == '__main__':
    check_for_all_app_updates()
