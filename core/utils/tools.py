# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import time


class Tools:
    @staticmethod
    def get_elapsed_time(start_time):
        return round((time.time() - start_time), 4)