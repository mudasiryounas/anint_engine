# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
from datetime import datetime

from core import db_session
from core.db_models import IPv4s, IPv6s, IPBlocks


class IpUtils:
    @staticmethod
    def save_ipv4s(app_id, ipv4_list):
        for ipv4 in ipv4_list:
            ip_location_result = {}
            ip_entity = IPv4s(app_id=app_id,
                              ip=ipv4,
                              asn_name=ip_location_result.get('AsnName'),
                              city_name=ip_location_result.get('CityName'),
                              country_name=ip_location_result.get('CountryName'),
                              region_name=ip_location_result.get('RegionName'),
                              zipcode=ip_location_result.get('ZipCode'),
                              longitude=ip_location_result.get('Longitude'),
                              latitude=ip_location_result.get('Latitude'),
                              insert_date=datetime.utcnow(),
                              update_date=datetime.utcnow())
            db_session.add(ip_entity)
        db_session.commit()

    @staticmethod
    def save_ipv6s(app_id, ipv6_list):
        for ipv6 in ipv6_list:
            ip_entity = IPv6s(app_id=app_id,
                              ip=ipv6,
                              insert_date=datetime.utcnow(),
                              update_date=datetime.utcnow())
            db_session.add(ip_entity)
        db_session.commit()

    @staticmethod
    def save_ipblocks(app_id, ipblock_list):
        for ip_block in ipblock_list:
            ipblock_entity = IPBlocks(app_id=app_id,
                                      ip_block=ip_block,
                                      insert_date=datetime.utcnow(),
                                      update_date=datetime.utcnow())
            db_session.add(ipblock_entity)
        db_session.commit()
