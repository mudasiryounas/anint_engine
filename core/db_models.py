#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from _datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from core import db_base


class Apps(db_base):
    __tablename__ = 'apps'
    id = Column(Integer(), primary_key=True)
    package = Column(String(), unique=True)
    platform_build_version_code = Column(String())
    platform_build_version_name = Column(String())
    name = Column(String())
    url = Column(String())
    published = Column(Boolean())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


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


class Hashes(db_base):
    __tablename__ = 'hashes'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    hash = Column(String())
    hash_type = Column(String())
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


class MacAddresses(db_base):
    __tablename__ = 'macaddresses'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    macaddress = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class BitcoinAddresses(db_base):
    __tablename__ = 'bitcoinaddresses'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    bitcoin_address = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class Cves(db_base):
    __tablename__ = 'cves'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    cve = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class GoogleAdsenseIds(db_base):
    __tablename__ = 'googleadsense'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    adsense_id = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class GoogleAnalyticsIds(db_base):
    __tablename__ = 'googleanalytics'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    analytic_id = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class TCKNs(db_base):
    __tablename__ = 'tckns'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    tckn = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class XmppAccounts(db_base):
    __tablename__ = 'xmppaccounts'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    xmpp_account = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class PhoneNumbers(db_base):
    __tablename__ = 'phonenumbers'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    phone_number = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class AttackTactics(db_base):
    __tablename__ = 'attacktactics'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    attack_tactic = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class AttackTechniques(db_base):
    __tablename__ = 'attacktechniques'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    attach_techniques = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class Asns(db_base):
    __tablename__ = 'asns'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    asn = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())


class UserAgents(db_base):
    __tablename__ = 'useragents'
    id = Column(Integer(), primary_key=True)
    app_id = Column(Integer(), ForeignKey(Apps.id), nullable=False, index=True)
    user_agent = Column(String())
    insert_date = Column(DateTime(), default=datetime.utcnow())
    update_date = Column(DateTime(), onupdate=datetime.utcnow())
