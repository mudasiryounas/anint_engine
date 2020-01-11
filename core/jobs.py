# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from core import db_session
from core.db_models import Apps
from core.utils.app_utils import AppUtils
from core.utils.playstore_utils import PlaystoreUtils


def check_for_app_updates(package):
    current_app_on_db = AppUtils.get_app(package)
    continue_job = False
    if current_app_on_db is None:
        print(f"Job is running first time for app: '{package}'")
        AppUtils.add_new_app(package)
        continue_job = True
    else:
        # check if application version is updated from playstore
        latest_playstore_app = PlaystoreUtils.get_app_latest_info(package)
        if current_app_on_db.version != latest_playstore_app.version:
            # if application version is updated, process latest apk
            print(f"New version is detected for app: '{package}'")
            continue_job = True
        # update application details on db, even if version is not updated, in order to keep application details history
        AppUtils.update_app(package, latest_playstore_app)

    if continue_job:
        print(f"Following app will be downloaded, decompiled and processed, app: '{package}'")
        # download latest apk
        # decompile latest apk
        # process latest decompiled files
    else:
        print(f"No new version is detected for app: '{package}'")


if __name__ == '__main__':
    check_for_app_updates('com.mys3soft.mys3chat')
