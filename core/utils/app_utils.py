# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import copy
from datetime import datetime

from core import db_session
from core.db_models import Apps, AppImages, AppHistory, AppCategories
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
            app = Apps(package=package,
                       title=ps_app['title'],
                       developer_id=ps_app['developer_id'],
                       developer_email=ps_app['developer_email'],
                       developer=ps_app['developer'],
                       developer_url=ps_app['developer_url'],
                       developer_address=ps_app['developer_address'],
                       description=ps_app['description'],
                       recent_changes=ps_app['recent_changes'],
                       editors_choice=ps_app['editors_choice'],
                       video=ps_app['video'],
                       score=ps_app['score'],
                       reviews=ps_app['reviews'],
                       icon=ps_app['icon'],
                       price=ps_app['price'],
                       url=ps_app['url'],
                       updated=ps_app['updated'],
                       current_version=ps_app['current_version'],
                       free=ps_app['free'],
                       size=ps_app['size'],
                       installs=ps_app['installs'],
                       required_android_version=ps_app['required_android_version'],
                       content_rating='|'.join(ps_app['content_rating']),
                       iap_range=ps_app['iap_range'],
                       interactive_elements=ps_app['interactive_elements'],
                       insert_date=datetime.utcnow(),
                       update_date=datetime.utcnow())

            db_session.add(app)
            db_session.flush()

            for category in ps_app['category']:
                app_category = AppCategories(app_id=app.id, category=category)
                db_session.add(app_category)

            for screenshot in ps_app['screenshots']:
                app_image = AppImages(app_id=app.id, image_url=screenshot)
                db_session.add(app_image)

            db_session.commit()
            print(f"New app added, id: '{app.id}', package: '{app.package}'")
            return app

    @staticmethod
    def update_app(package, ps_app):
        app = db_session.query(Apps).filter_by(package=package).first()
        app_before_update = copy.deepcopy(app)
        messages = []
        exclude_attrs = ['id', 'insert_date', 'update_date', 'metadata', 'package', 'platform_build_version_code', 'platform_build_version_name', 'published']
        app_attrs = [item for item in dir(app) if not item.startswith('_') and item not in exclude_attrs ]
        for attr_name in app_attrs:
            app_attr_value = getattr(app, attr_name)
            ps_app_attr_value = ps_app[attr_name]
            if attr_name == 'content_rating':
                ps_app_attr_value = '|'.join(ps_app_attr_value)
            if app_attr_value != ps_app_attr_value:
                messages.append(f"app '{attr_name}' is changed from '{app_attr_value}' to '{ps_app_attr_value}'")
                setattr(app, attr_name, ps_app_attr_value)

        # keep application history
        if len(messages) > 0:
            app.update_date = datetime.utcnow()
            app_history = AppHistory(app_id=app_before_update.id,
                                     package=app_before_update.package,
                                     platform_build_version_code=app_before_update.platform_build_version_code,
                                     platform_build_version_name=app_before_update.platform_build_version_name,
                                     title=app_before_update.title,
                                     developer_id=app_before_update.developer_id,
                                     developer_email=app_before_update.developer_email,
                                     developer=app_before_update.developer,
                                     developer_url=app_before_update.developer_url,
                                     developer_address=app_before_update.developer_address,
                                     description=app_before_update.description,
                                     recent_changes=app_before_update.recent_changes,
                                     editors_choice=app_before_update.editors_choice,
                                     video=app_before_update.video,
                                     score=app_before_update.score,
                                     reviews=app_before_update.reviews,
                                     icon=app_before_update.icon,
                                     price=app_before_update.price,
                                     url=app_before_update.url,
                                     updated=app_before_update.updated,
                                     current_version=app_before_update.current_version,
                                     free=app_before_update.free,
                                     size=app_before_update.size,
                                     installs=app_before_update.installs,
                                     published=app_before_update.published,
                                     required_android_version=app_before_update.required_android_version,
                                     content_rating=app_before_update.content_rating,
                                     iap_range=app_before_update.iap_range,
                                     interactive_elements=app_before_update.interactive_elements,
                                     messages=' | '.join(messages),
                                     insert_date=datetime.utcnow())
            db_session.add(app_history)
            db_session.commit()
            print(f"Following app is updated and a new record for history is added, app: '{package}'")
