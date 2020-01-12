# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from enum import Enum


class AppsToFollowStatus(Enum):
    WAITING = 1
    NEW_VERSION_DETECTED = 2
    WAITING_DOWNLOAD = 3
    DOWNLOADING = 4
    DOWNLOADED = 5
    DECOMPILING = 6
    DECOMPILED = 7
    PROCESSING = 8
    PROCESSED = 9

    ERROR = 99


class LogType(Enum):
    DOWNLOAD = 'DOWNLOAD'
    DECOMPILE = 'DECOMPILE'
