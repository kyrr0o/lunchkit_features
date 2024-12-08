

from src.database import db_connection
import pymysql.cursors

class Store:

    @staticmethod
    def create_store(StoreName,StoreOwnerId, StoreApplicationId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO Store (StoreName,StoreOwnerId, StoreApplicationId) VALUES (%s,%s,%s)"
        sqlValues = (StoreName,StoreOwnerId, StoreApplicationId)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_store_details(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM Store WHERE StoreOwnerId = %s"
        sqlValues = (StoreOwnerId,)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        store_details = cursor.fetchone()
        cursor.close()
        connection.close()
        return store_details
    
    @staticmethod
    def get_store_details_storeId(StoreId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM Store WHERE StoreId = %s"
        sqlValues = (StoreId,)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        store_details = cursor.fetchone()
        cursor.close()
        connection.close()
        return store_details

    
    @staticmethod
    def get_stores():
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM Store")
        stores = cursor.fetchall()
        cursor.close()
        connection.close()
        return stores
    
        
