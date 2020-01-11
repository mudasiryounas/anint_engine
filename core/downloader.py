# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential


from core.utils.app_utils import AppUtils


def download_apk(package):
    # check if app is in db, add new otherwise
    app = AppUtils.get_app(package=package)
    if not app:
        app = AppUtils.add_new_app(package=package)

    # download app





if __name__ == '__main__':
    download_apk(package='com.mys3soft.mys3chat')
