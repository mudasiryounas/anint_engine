#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from core.processors.apk_processor import decompile_apk

if __name__ == '__main__':
    file_path = '/tmp/anint/mys3chat/mys3chat.apk'
    decompile_apk(file_path)
