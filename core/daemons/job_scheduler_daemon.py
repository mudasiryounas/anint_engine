# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import os
import time

from core import db_session
from core.db_models import AppsToFollow
from core.jobs.check_for_app_updates import check_for_app_updates


def job_scheduler_daemon():
    print(f"Job scheduler daemon started for first time")
    sleep_seconds = 24 * 60 * 60  # 24 hours
    while True:
        try:
            apps_to_follow = db_session.query(AppsToFollow).all()
            apps_to_follow_packages = [item.package for item in apps_to_follow]
            print(f"Adding '{len(apps_to_follow_packages)}' apps to queue for checking updates")
            for package in apps_to_follow_packages:
                check_for_app_updates(package)
            print(f"Sleeping for '{sleep_seconds}' seconds before triggering a new jobs")
            time.sleep(sleep_seconds)
        except KeyboardInterrupt as e:
            print("Keyboard interrupt is taken, stopping the job scheduler daemon.")
            break
        except Exception as e:
            print(f"Exception at job scheduler daemon, Exception: '{e}'")
            os._exit(-1)


if __name__ == '__main__':
    job_scheduler_daemon()
