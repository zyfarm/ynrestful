# -*- coding: utf-8 -*-


import ConfigParser
import logging
import logging.config
import os
from project.config.meta_config import DB_CONFIG, DEPLOY_MODE, CACHE_CONFIG
import redis
from sqlalchemy import create_engine

__author__ = 'jiyue'


class ConfigInitor(object):
    db_engine = None
    redis_client = None
    main_logger = logging.getLogger('main')

    @staticmethod
    def config_parser(file):
        config_dir = os.path.dirname(__file__)
        project_dir = os.path.dirname(os.path.dirname(config_dir))
        config_file_path = os.path.join(project_dir, file)
        cf = ConfigParser.ConfigParser()
        try:
            cf.read(config_file_path)
            logging.config.fileConfig(file)
            DB_CONFIG.db_name = cf.get('db', 'db_name')
            DB_CONFIG.db_password = cf.get('db', 'db_password')
            DB_CONFIG.db_host = cf.get('db', 'db_host')
            DB_CONFIG.db_port = cf.get('db', 'db_port')
            DB_CONFIG.db_type = cf.get('db', 'db_type')
            DB_CONFIG.db_user = cf.get('db', 'db_user')

            DEPLOY_MODE.debug = cf.get('debug', 'debug')
            CACHE_CONFIG.cache_host = cf.get('cache', 'cache_host')
            CACHE_CONFIG.cache_port = cf.get('cache', 'cache_port')

            db_url = DB_CONFIG.db_type + "://" + DB_CONFIG.db_user + ":" \
                     + DB_CONFIG.db_password + "@" + DB_CONFIG.db_host + ":" + DB_CONFIG.db_port + "/" + DB_CONFIG.db_name + "?charset=utf8"

            ConfigInitor.db_engine = create_engine(db_url, connect_args={'charset': 'utf8'})
            ConfigInitor.main_logger.info("db init success:%s", db_url)

            ConfigInitor.redis_client = redis.StrictRedis(host=CACHE_CONFIG.cache_host, port=CACHE_CONFIG.cache_port,
                                                          db=0)

            ConfigInitor.main_logger.info("cache init success:%s:%s", CACHE_CONFIG.cache_host, CACHE_CONFIG.cache_port)
        except Exception, e:
            ConfigInitor.main_logger.error("config file load error:%s", e.message)
            raise IOError('not valid config file')
