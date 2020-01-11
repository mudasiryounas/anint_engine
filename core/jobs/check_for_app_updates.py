# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from core.utils.app_utils import AppUtils
from core.utils.playstore_utils import PlaystoreUtils


def download_latest_apk(package, version):
    pass


def check_for_app_updates(package):
    current_app_on_db = AppUtils.get_app(package)
    new_version = None
    if current_app_on_db is None:
        print(f"Job is running first time for app: '{package}'")
        added_app = AppUtils.add_new_app(package)
        new_version = added_app.current_version
    else:
        # check if application version is updated from playstore
        latest_playstore_app = PlaystoreUtils.get_app_latest_info(package)
        if current_app_on_db.current_version != latest_playstore_app['current_version']:
            # if application version is updated, process latest apk
            print(f"New version is detected for app: '{package}', new version: '{latest_playstore_app['current_version']}'")
            new_version = latest_playstore_app['current_version']
        # update application details on db, even if version is not updated, in order to keep application details history
        AppUtils.update_app(package, latest_playstore_app)

    if new_version:
        print(f"Following app will be downloaded, decompiled and processed, app: '{package}', version: '{new_version}'")
        download_latest_apk(package, new_version)
        # decompile latest apk
        # process latest decompiled files
    else:
        print(f"No new version is detected for app: '{package}'")


if __name__ == '__main__':
    check_for_app_updates('com.mys3soft.mys3chat')
