# -*- coding: utf-8 -*-
from pymongo import MongoClient
from time import strftime
from time import localtime


class MongoDBConnect(object):
    def __init__(self,
                 mongo_host='127.0.0.1',
                 mongo_port=27017,
                 mongo_database='ScrapyRabbitLog',
                 mongo_table=strftime("%Y%m%d", localtime()),
                 mongo_username=None,
                 mongo_password=None,
                 scrapy_object=None
                 ):

        self.__mongo_host = scrapy_object.mongo_host if scrapy_object else mongo_host
        self.__mongo_port = scrapy_object.mongo_port if scrapy_object else mongo_port
        self.__mongo_database = scrapy_object.mongo_database if scrapy_object else mongo_database
        self.__mongo_table = scrapy_object.mongo_table if scrapy_object else mongo_table
        self.__mongo_username = scrapy_object.mongo_username if scrapy_object else mongo_username
        self.__mongo_password = scrapy_object.mongo_password if scrapy_object else mongo_password

        conn_mgo = MongoClient(self.__mongo_host, self.__mongo_port)
        db = conn_mgo[self.__mongo_database]
        if self.__mongo_username and self.__mongo_password:
            db.authenticate(mongo_username, mongo_password)
        self.__collection = db[self.__mongo_table]

    def insert(self, log_data):
        self.__collection.insert_one(log_data)
