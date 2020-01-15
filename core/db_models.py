# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from _datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy_utils.types import TSVectorType

from core import db_base


class AppsToFollow(db_base):
    __tablename__ = 'apps_to_follow'
    id = Column(Integer(), primary_key=True)
    package = Column(String(), unique=True, nullable=False)
    last_version = Column(String())
    current_version = Column(String())
    app_to_follow_status = Column(Integer())
    inserted_by = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class Apps(db_base):
    __tablename__ = 'apps'
    id = Column(Integer(), primary_key=True)
    package = Column(String(), unique=True)
    platform_build_version_code = Column(String())
    platform_build_version_name = Column(String())
    title = Column(String())
    developer_id = Column(String())
    developer_email = Column(String())
    developer = Column(String())
    developer_url = Column(String())
    developer_address = Column(String())
    description = Column(String())  # todo make full text search
    recent_changes = Column(String())
    editors_choice = Column(Boolean())
    video = Column(String())
    score = Column(String())
    reviews = Column(Integer())
    icon = Column(String())
    price = Column(String())
    url = Column(String())
    updated = Column(String())
    current_version = Column(String())
    free = Column(Boolean())
    size = Column(String())
    installs = Column(String())
    published = Column(Boolean())
    required_android_version = Column(String())
    content_rating = Column(String())
    iap_range = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class AppHistory(db_base):
    __tablename__ = 'app_history'
    id = Column(Integer(), primary_key=True)
    insert_date = Column(DateTime(), default=datetime.utcnow())
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    package = Column(String())
    platform_build_version_code = Column(String())
    platform_build_version_name = Column(String())
    title = Column(String())
    developer_id = Column(String())
    developer_email = Column(String())
    developer = Column(String())
    developer_url = Column(String())
    developer_address = Column(String())
    description = Column(String())
    recent_changes = Column(String())
    editors_choice = Column(Boolean())
    video = Column(String())
    score = Column(String())
    reviews = Column(Integer())
    icon = Column(String())
    price = Column(String())
    url = Column(String())
    updated = Column(String())
    current_version = Column(String())
    free = Column(Boolean())
    size = Column(String())
    installs = Column(String())
    published = Column(Boolean())
    required_android_version = Column(String())
    content_rating = Column(String())
    iap_range = Column(String())
    messages = Column(String())


class AppContents(db_base):
    __tablename__ = 'app_contents'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    content = Column(String())  # must be maximum of 1 MB for full text search
    content_file = Column(String())
    app_version = Column(String())
    content_status = Column(Integer())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), default=datetime.utcnow())
    search_vector = Column(TSVectorType('content'))
    __table_args__ = (
        Index(
            'idx_app_content_search_vector',
            search_vector,
            postgresql_using='gin'
        ),
    )


class AppImages(db_base):
    __tablename__ = 'app_images'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    image_url = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())


class AppCategories(db_base):
    __tablename__ = 'app_categories'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    category = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())


class AppSDKs(db_base):
    __tablename__ = 'app_sdks'
    id = Column(Integer(), primary_key=True)
    insert_date = Column(DateTime(), default=datetime.utcnow())
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    sdk = Column(String())
    version = Column(String())
    sdk_detail_link = Column(String())


class AppActivities(db_base):
    __tablename__ = 'app_activities'
    id = Column(Integer(), primary_key=True)
    insert_date = Column(DateTime(), default=datetime.utcnow())
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    activity = Column(String())


class AppServicess(db_base):
    __tablename__ = 'app_servicess'
    id = Column(Integer(), primary_key=True)
    insert_date = Column(DateTime(), default=datetime.utcnow())
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    service = Column(String())


class AppPermissions(db_base):
    __tablename__ = 'app_permissions'
    id = Column(Integer(), primary_key=True)
    insert_date = Column(DateTime(), default=datetime.utcnow())
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    permission = Column(String())


class AppServices(db_base):
    __tablename__ = 'app_services'
    id = Column(Integer(), primary_key=True)
    insert_date = Column(DateTime(), default=datetime.utcnow())
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    service = Column(String())


class AppReceivers(db_base):
    __tablename__ = 'app_receivers'
    id = Column(Integer(), primary_key=True)
    insert_date = Column(DateTime(), default=datetime.utcnow())
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    receiver = Column(String())


class Urls(db_base):
    __tablename__ = 'urls'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    url = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class Emails(db_base):
    __tablename__ = 'emails'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    email = Column(String())
    domain = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class Domains(db_base):
    __tablename__ = 'domains'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    domain = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class CreditCards(db_base):
    __tablename__ = 'creditcards'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    card_number = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class IPv4s(db_base):
    __tablename__ = 'ipv4s'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    ip = Column(String())
    asn_name = Column(String())
    city_name = Column(String())
    country_name = Column(String())
    region_name = Column(String())
    zipcode = Column(String())
    longitude = Column(String())
    latitude = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class IPv6s(db_base):
    __tablename__ = 'ipv6s'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    ip = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class IPBlocks(db_base):
    __tablename__ = 'ipblocks'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    ip_block = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class PhoneNumbers(db_base):
    __tablename__ = 'phonenumbers'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    phone_number = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())
