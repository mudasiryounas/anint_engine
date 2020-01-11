# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import copy
from datetime import datetime

from core import db_session
from core.db_models import Apps, AppImages, AppHistory
from core.utils.playstore_utils import PlaystoreUtils


class AppUtils:

    @staticmethod
    def get_app(package):
        app = db_session.query(Apps).filter_by(package=package).first()
        return app

    @staticmethod
    def add_new_app(package):
        app = AppUtils.get_app(package=package)
        if app is None:
            ps_app = PlaystoreUtils.get_app_latest_info(package)
            app = Apps(package=package, name=ps_app.name, category=ps_app.category, free=ps_app.free, developer_name=ps_app.developer_name,
                       description=ps_app.description, logo=ps_app.logo, price=ps_app.price, developer_email=ps_app.developer_email, developer_website=ps_app.developer_website,
                       rating=ps_app.rating, reviews=ps_app.reviews, updated=ps_app.updated, version=ps_app.version, insert_date=datetime.utcnow(), update_date=datetime.utcnow())

            db_session.add(app)
            db_session.flush()

            for image_url in ps_app.images:
                app_detail = AppImages(app_id=app.id, image_url=image_url)
                db_session.add(app_detail)

            db_session.commit()
            print(f"New app added, id: '{app.id}', package: '{app.package}'")
            return app

    @staticmethod
    def update_app(package, ps_app):
        app = db_session.query(Apps).filter_by(package=package).first()
        app_before_update = copy.deepcopy(app)
        updated = False

        if app.name != ps_app.name:
            updated = True
            app.name = ps_app.name

        if app.category != ps_app.category:
            updated = True
            app.category = ps_app.category

        if app.developer_name != ps_app.developer_name:
            updated = True
            app.developer_name = ps_app.developer_name

        if app.developer_email != ps_app.developer_email:
            updated = True
            app.developer_email = ps_app.developer_email

        if app.developer_website != ps_app.developer_website:
            updated = True
            app.developer_website = ps_app.developer_website

        if app.description != ps_app.description:
            updated = True
            app.description = ps_app.description

        if float(app.rating) != float(ps_app.rating):
            updated = True
            app.rating = ps_app.rating

        if app.reviews != ps_app.reviews:
            updated = True
            app.reviews = ps_app.reviews

        if app.logo != ps_app.logo:
            updated = True
            app.logo = ps_app.logo

        if app.price != ps_app.price:
            updated = True
            app.price = ps_app.price

        if app.updated != ps_app.updated:
            updated = True
            app.updated = ps_app.updated

        if app.version != ps_app.version:
            updated = True
            app.version = ps_app.version

        if app.free != ps_app.free:
            updated = True
            app.free = ps_app.free

        # keep application history
        if updated:
            app.update_date = datetime.utcnow()
            app_history = AppHistory(app_id=app_before_update.id, package=app_before_update.package, name=app_before_update.name, category=app_before_update.category,
                                     free=app_before_update.free, developer_name=app_before_update.developer_name, description=app_before_update.description,
                                     logo=app_before_update.logo, price=app_before_update.price, developer_email=app_before_update.developer_email,
                                     developer_website=app_before_update.developer_website, rating=app_before_update.rating, reviews=app_before_update.reviews,
                                     updated=app_before_update.updated, version=app_before_update.version, insert_date=datetime.utcnow())
            db_session.add(app_history)
            db_session.commit()
            print(f"Following app is updated and a new record for history is added, app: '{package}'")
