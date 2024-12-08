from src.database import db_connection
import pymysql.cursors

class Item:

    @staticmethod
    def get_items():
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        cursor.close()
        connection.close()
        return items
    
    @staticmethod
    def get_storeItems(StoreId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        SqlQuery = "SELECT * FROM items WHERE StoreId = %s"
        SqlValues = (StoreId,)
        cursor.execute(SqlQuery, SqlValues)
        store_items = cursor.fetchall()
        cursor.close()
        connection.close()
        return store_items
    
    @staticmethod
    def add_item(ItemName, ItemDescription, ItemPrice, ItemPhoto, StoreId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        SqlQuery= '''INSERT INTO items (ItemName, ItemDescription, ItemPrice, itemPhoto, StoreId)
                        VALUES (%s, %s, %s, %s, %s)'''
        SqlValues = (ItemName, ItemDescription, ItemPrice, ItemPhoto, StoreId)
        cursor.execute(SqlQuery, SqlValues)
        connection.commit()
        cursor.close()
        connection.close()
        return Item.get_items()
        
        
    