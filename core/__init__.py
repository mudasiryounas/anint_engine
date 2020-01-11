#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2020 Android Intelligence - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
import configparser

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = configparser.ConfigParser()
config.read('./config/dev.cfg')
db_conn_string = config['DEFAULT']['SQLALCHEMY_DATABASE_URI']
db = create_engine(db_conn_string, echo=True)
db_base = declarative_base()
Session = sessionmaker(db)
db_session = Session()