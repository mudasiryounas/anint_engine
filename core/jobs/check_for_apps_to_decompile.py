# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import subprocess
import time

from core import db_session
from core.Enums import AppsToFollowStatus
from core.db_models import AppsToFollow

DECOMPILED_FILES_OUTPUT_FOLDER = '/tmp/anint/decompiled_apks'
DOWNLOADED_APK_FOLDER = '/tmp/anint/downloaded_apks'


def decompile_app(package, version):
    print(f"Decompiling started for app: '{package}', version: '{version}'")
    decompile_start_time = time.time()
    downloaded_apk_folder = DOWNLOADED_APK_FOLDER + '/' + package + '/' + version + '.apk'
    decompiled_files_output_folder = DECOMPILED_FILES_OUTPUT_FOLDER + '/' + package + '/' + version

    # Use -f switch if you want to overwrite if folder already exists
    command_to_run = ['java', '-jar', '/usr/local/bin/apktool.jar', 'decode', downloaded_apk_folder, '-o', decompiled_files_output_folder]
    print(f"Command to execute: '{' '.join(command_to_run)}'")
    command_start_time = time.time()
    res = subprocess.run(command_to_run)
    print(f"Command executed, took '{round((time.time() - command_start_time), 4)} seconds, returncode : '{res.returncode}'")

    # update DECOMPILED status in db
    apps_to_follow = db_session.query(AppsToFollow).filter_by(package=package).first()
    apps_to_follow.status = AppsToFollowStatus.DECOMPILED.value
    db_session.commit()
    print(f"Decompiling finished for app: '{package}', version: '{version}', Took '{round((time.time() - decompile_start_time), 4)}' seconds")


def check_for_apps_to_decompile():
    start_time = time.time()
    print(f"Check for apps to decompile job started")
    apps_to_decompile = db_session.query(AppsToFollow).filter_by(status=AppsToFollowStatus.DOWNLOADED.value).all()
    if apps_to_decompile:
        apps_to_decompile_tuple = [(item.package, item.current_version) for item in apps_to_decompile]
        for item in apps_to_decompile:
            item.status = AppsToFollowStatus.DECOMPILING.value
        db_session.commit()
        for package, current_version in apps_to_decompile_tuple:
            decompile_app(package, current_version)
    print(f"Check for apps to decompile job finished, Took '{round((time.time() - start_time), 4)}' seconds")


if __name__ == '__main__':
    check_for_apps_to_decompile()
