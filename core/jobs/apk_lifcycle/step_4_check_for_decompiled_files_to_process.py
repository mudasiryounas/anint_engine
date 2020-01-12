# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime

from core import db_session
from core.Enums import AppsToFollowStatus, ContentStatus
from core.db_models import AppsToFollow, AppContents
from core.utils.tools import Tools
from core.utils.app_utils import AppUtils

DECOMPILED_FILES_FOLDER = '/tmp/anint/decompiled_apks'

EXCLUDED_FILE_EXTENSION = ['png', 'webp', 'ttf', 'kotlin_metadata', 'kotlin_builtins', 'kotlin_module', 'RSA', 'gz']


def process_manifest_file(package, folder_path):
    def __get_value_by_attr_name(item, attr_name):
        for key, value in item.attrib.items():
            if key.endswith(attr_name):
                return value

    manifest_file_path = folder_path + '/AndroidManifest.xml'
    root = ET.parse(manifest_file_path).getroot()
    platform_build_version_code = root.get('platformBuildVersionCode')
    platform_build_version_name = root.get('platformBuildVersionName')

    permission_list = []
    activity_list = []
    service_list = []
    receiver_list = []

    for elem in root:
        if elem.tag == 'uses-permission':
            permission_list.append(__get_value_by_attr_name(elem, 'name'))
        elif elem.tag == 'application':
            for sub_item in elem:
                if sub_item.tag == 'activity':
                    activity_list.append(__get_value_by_attr_name(sub_item, 'name'))
                elif sub_item.tag == 'service':
                    service_list.append(__get_value_by_attr_name(sub_item, 'name'))
                elif sub_item.tag == 'receiver':
                    receiver_list.append(__get_value_by_attr_name(sub_item, 'name'))

    AppUtils.add_app_permissions(package, permission_list)
    AppUtils.add_app_activities(package, activity_list)
    AppUtils.add_app_services(package, service_list)
    AppUtils.add_app_receivers(package, receiver_list)

    AppUtils.update_app_info(package=package, platform_build_version_code=platform_build_version_code, platform_build_version_name=platform_build_version_name)
    print(f"processing manifest file finished, for app: '{package}'")


def process_other_files(package, folder_path):
    # save files to 'contents' table to be processed by IOC 'step_4_check_for_contents_to_process'
    files_processing_start_time = time.time()
    app = AppUtils.get_app(package)
    app_id = app.id
    app_version = app.current_version
    db_commit_checkpoint = 0  # commit session after each 1000 new records
    for subdir, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.split('.')[-1] not in EXCLUDED_FILE_EXTENSION:
                file_full_path = subdir + os.sep + file_name
                app_level_file_path = file_full_path.replace(folder_path, '')
                with open(file_full_path, 'rt') as f:
                    try:
                        file_content = f.read()
                    except Exception as e:
                        print(f"Exception while reading file: '{file_full_path}', app: '{package}', Exception: '{str(e)}'")
                        continue
                each_text_size = 1000000  # 1 MB
                final_contents_to_save = []
                if len(file_content) > each_text_size:
                    print(f"More than 1 MB content found, splitting and saving maximum of 1 MB, app: '{package}', file: '{file_full_path}'")
                    split_texts = []
                    for i in range(0, len(file_content), each_text_size):
                        if i == 0:
                            split_texts.append(file_content[i:i + each_text_size])
                        else:
                            split_texts.append(file_content[i - 200:i + each_text_size])  # keep some words extra in order to not miss any word
                    for each_content in split_texts:
                        final_contents_to_save.append(each_content)
                else:
                    final_contents_to_save = [file_content]
                for final_content in final_contents_to_save:
                    final_content = final_content.replace(chr(0x00), "")
                    # check for duplicates
                    app_content = db_session.query(AppContents).filter_by(app_id=app_id, app_version=app_version, content_file=app_level_file_path).first()
                    if app_content is None:
                        app_content = AppContents(app_id=app_id, content=final_content, content_file=app_level_file_path, app_version=app_version, content_status=ContentStatus.UNPROCESSED.value, insert_date=datetime.utcnow())
                        db_session.add(app_content)
                        db_commit_checkpoint += 1
                if db_commit_checkpoint >= 1000:
                    print(f"Committing '{db_commit_checkpoint}' records...")
                    db_session.commit()
                    db_commit_checkpoint = 0
    db_session.commit()
    print(f"Processing other files finished for app: '{package}', Took '{Tools.get_elapsed_time(files_processing_start_time)}' seconds")


def process_app(package, version):
    processing_start_time = time.time()
    decompiled_files_output_folder = DECOMPILED_FILES_FOLDER + '/' + package + '/' + version
    process_manifest_file(package, decompiled_files_output_folder)
    process_other_files(package, decompiled_files_output_folder)
    # update PROCESSED status in db
    apps_to_follow = db_session.query(AppsToFollow).filter_by(package=package).first()
    apps_to_follow.status = AppsToFollowStatus.PROCESSED.value
    db_session.commit()
    print(f"Processing finished for app: '{package}', version: '{version}', Took '{Tools.get_elapsed_time(processing_start_time)}' seconds")


def main():
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
    print(f"Check for apps to process job finished, Took '{Tools.get_elapsed_time(start_time)}' seconds")


if __name__ == '__main__':
    # main()
    process_other_files('com.inovel.app.yemeksepeti', '/tmp/anint/decompiled_apks/com.inovel.app.yemeksepeti/3.1.9')
