#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import subprocess
import time
import xml.etree.ElementTree as ET
from datetime import datetime

from core import db_session
from core.db_models import Apps


def decompile_apk(file_path):
    print(f"Decompile started for file: '{file_path}")
    output_folder = file_path + '.out'
    # Use -f switch if you want to overwrite if folder already exists
    command_to_run = ['java', '-jar', '/usr/local/bin/apktool.jar', 'decode', file_path, '-o', output_folder]
    print(f"Command to execute: '{' '.join(command_to_run)}'")
    command_start_time = time.time()
    res = subprocess.run(command_to_run)
    print(f"Command executed, took '{round((time.time() - command_start_time), 3)} seconds, returncode : '{res.returncode}'")
    process_decompiled_folder(output_folder)
    print(f"Decompile finished for file: '{file_path}")


def process_decompiled_folder(folder_path):
    print("processing decompiled folder...")
    proccess_manifest_file(folder_path)
    print("processing decompiled folder finished.")


def proccess_manifest_file(folder_path):
    manifest_file_path = folder_path + '/AndroidManifest.xml'
    print(f"Processing manifest file from folder: '{manifest_file_path}'")
    root = ET.parse(manifest_file_path).getroot()
    package = root.get('package')
    platform_build_version_code = root.get('platformBuildVersionCode')
    platform_build_version_name = root.get('platformBuildVersionName')

    application = db_session.query(Apps).filter_by(package=package).first()
    if application is None:
        url = f'https://play.google.com/store/apps/details?id={package}'
        application = Apps(package=package, platform_build_version_code=platform_build_version_code, platform_build_version_name=platform_build_version_name,
                                   url=url, insert_date=datetime.utcnow(), update_date=datetime.utcnow())
        db_session.add(application)
        db_session.commit()
    print("processing manifest file finished.")
