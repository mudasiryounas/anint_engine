#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from core import db_session
from core.db_models import Apps, AppsDetail
from play_store import App

from core.utils.playstore_utils import PlaystoreUtils


class AppUtils:

    @staticmethod
    def get_app(package):
        app = db_session.query(Apps).filter_by(package=package).first()
        return app

    @staticmethod
    def add_new_app(package):
        try:
            app = AppUtils.get_app(package=package)
            if app is None:
                ps_app = PlaystoreUtils.get_app_info (package)
                app = Apps(package=package, name=ps_app.name, category=ps_app.category, free=ps_app.free, developer_name=ps_app.developer_name,
                           description=ps_app.description, logo=ps_app.logo, price=ps_app.price, developer_email=ps_app.developer_email, developer_website=ps_app.developer_website,
                           rating=ps_app.rating, reviews=ps_app.reviews, updated=ps_app.updated, current_version=ps_app.version)

                db_session.add(app)
                db_session.flush()

                for image in ps_app.images:
                    app_detail = AppsDetail(app_id=app.id, image=image)
                    db_session.add(app_detail)

                db_session.commit()
                app.images = ps_app.images
                print(f"New app added, id: '{app.id}', package: '{app.package}'")
                return app
            return None
        except Exception as e:
            print(f"Exception while getting app info from playstore, Exception: '{str(e)}' ")
            return None


