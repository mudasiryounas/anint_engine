# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import time
import xml.etree.ElementTree as ET

from core import db_session
from core.Enums import AppsToFollowStatus
from core.db_models import AppsToFollow
from core.utils.app_utils import AppUtils

DECOMPILED_FILES_FOLDER = '/tmp/anint/decompiled_apks'


def process_manifest_file(package, folder_path):
    manifest_file_path = folder_path + '/AndroidManifest.xml'
    print(f"Processing following manifest file: '{manifest_file_path}'")
    root = ET.parse(manifest_file_path).getroot()
    platform_build_version_code = root.get('platformBuildVersionCode')
    platform_build_version_name = root.get('platformBuildVersionName')

    permission_list = root.get('uses-permission')
    activity_list = []
    service_list = []
    receiver_list = []

    AppUtils.add_app_permissions(package, permission_list)
    AppUtils.add_app_activities(package, activity_list)
    AppUtils.add_app_services(package, service_list)
    AppUtils.add_app_receivers(package, receiver_list)

    AppUtils.update_app_info(package=package, platform_build_version_code=platform_build_version_code, platform_build_version_name=platform_build_version_name)
    print("processing manifest file finished.")


def process_app(package, version):
    print(f"Processing started for app: '{package}', version: '{version}'")
    processing_start_time = time.time()
    decompiled_files_output_folder = DECOMPILED_FILES_FOLDER + '/' + package + '/' + version
    process_manifest_file(package, decompiled_files_output_folder)
    # update PROCESSED status in db
    apps_to_follow = db_session.query(AppsToFollow).filter_by(package=package).first()
    apps_to_follow.status = AppsToFollowStatus.PROCESSED.value
    db_session.commit()
    print(f"Processing finished for app: '{package}', version: '{version}', Took '{round((time.time() - processing_start_time), 4)}' seconds")


def check_for_apps_to_process():
    start_time = time.time()
    print(f"Check for apps to process job started")
    apps_to_process = db_session.query(AppsToFollow).filter_by(status=AppsToFollowStatus.DECOMPILED.value).all()
    if apps_to_process:
        apps_to_process_tuple = [(item.package, item.current_version) for item in apps_to_process]
        for item in apps_to_process:
            item.status = AppsToFollowStatus.PROCESSING.value
        db_session.commit()
        for package, current_version in apps_to_process_tuple:
            process_app(package, current_version)
    print(f"Check for apps to process job finished, Took '{round((time.time() - start_time), 4)}' seconds")


if __name__ == '__main__':
    process_manifest_file('com.mys3soft.mys3chat', '/tmp/anint/decompiled_apks/com.mys3soft.mys3chat/3.8')
