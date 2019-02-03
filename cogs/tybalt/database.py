import discord
import os
import mysql.connector
from __main__ import settings

class database():
    connection = None
    cursor = None
    
    @staticmethod
    def verify_connection():
        cnx = database.get_connection()
        if cnx.is_connected() == False:
            cnx.reconnect()
            database.cursor = None


    @staticmethod
    def get_connection():
        if database.connection is None:
            dbconfig = settings.bot_settings['DATABASE']
            database.connection = mysql.connector.connect(user=dbconfig['USER'], password=dbconfig['PASS'], host=dbconfig['HOST'], database=dbconfig['BASE'])
        return database.connection

    @staticmethod
    def get_cursor():
        if database.cursor is None:
            cnx = database.get_connection()
            database.cursor = cnx.cursor()
        return database.cursor

