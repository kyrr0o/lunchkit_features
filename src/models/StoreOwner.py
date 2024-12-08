"""
Store Owner Model Module
-----------------------

This module handles database operations for store owners, providing methods
for creating, searching, and managing store owner records.

Key Components:
    - Database CRUD operations for store owners
    - Password hashing integration
    - Email-based owner lookup

Methods:
    - create_storeOwner: Create new store owner record
    - search_storeOwner: Find store owner by email
    - delete_storeOwner: Remove store owner record

"""
from src.database import db_connection
import pymysql.cursors




class StoreOwner:

    @staticmethod
    def create_storeOwner(OwnerName,Email,MobileNum,Password,ApplicationStatus):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO STOREOWNERS (OwnerName,Email,Mobile_Num,Password,Application_Status) VALUES (%s,%s,%s,%s,%s)"
        sqlValues = (OwnerName,Email,MobileNum,Password,ApplicationStatus)
        cursor.execute(sqlQuery,sqlValues)
        connection.commit()
        cursor.close()
        connection.close()


    @staticmethod
    def search_storeOwner(email):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreOwners WHERE EMAIL = %s"
        sqlValues = (email,)
        cursor.execute(sqlQuery,sqlValues)
        owner = cursor.fetchone()
        cursor.close()
        connection.close()
        return owner
    
    @staticmethod
    def search_storeOwnerWithId(storeOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreOwners WHERE StoreOwnerId = %s"
        sqlValues = (storeOwnerId,)
        cursor.execute(sqlQuery,sqlValues)
        owner = cursor.fetchone()
        cursor.close()
        connection.close()
        return owner
    

    @staticmethod
    def delete_storeOwner(email):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "DELETE FROM StoreOwners WHERE EMAIL = %s"
        sqlValue = (email,)
        cursor.execute(sqlQuery,sqlValue)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update_storeOwner(email, OwnerName, MobileNum, Password, ApplicationStatus):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE StoreOwners SET OwnerName = %s,Mobile_Num = %s,Password = %s,Application_Status = %s WHERE Email = %s"
        sqlValues = (OwnerName, MobileNum, Password, ApplicationStatus, email)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def update_storeOwner_application_processing(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE StoreOwners SET Application_Status = 'Processing' WHERE StoreOwnerId = %s"
        sqlValues = (StoreOwnerId,)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        cursor.close()
        connection.close()


    @staticmethod
    def get_pending_store_owner():
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreOwners S JOIN StoreApplications A on S.StoreOwnerId = A.StoreOwnerId"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    

    @staticmethod
    def get_preview_store_owner():
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreApplications S JOIN ApplicationDocuments A on S.StoreApplicationId = A.StoreApplicationId"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    
    @staticmethod
    def get_store_owner_verification(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE StoreOwners SET Application_Status = 'Completed' WHERE StoreOwnerId = %s"
        sqlValues = (StoreOwnerId,)
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result
    
    @staticmethod
    def get_store_application_verification(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE StoreApplications SET ApplicationStatus = 'Approved' WHERE StoreOwnerId = %s"
        sqlValues = (StoreOwnerId,)
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        return result

    @staticmethod
    def search_storeApplicationId(StoreApplicationId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM ApplicationDocuments WHERE StoreApplicationId = %s"
        sqlValues = (StoreApplicationId,)
        cursor.execute(sqlQuery,sqlValues)
        connection.commit()
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    
    @staticmethod
    def get_approvedStores():
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreOwners WHERE Application_Status = 'Completed'"
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    

    @staticmethod
    def set_profile_picture(StoreOwnerId):
            connection = db_connection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE Shop SET ShopPhoto = %s WHERE shopId = %s"
            sqlValues = ("/src/static/img/default_picture.jpg", StoreOwnerId)
            cursor.execute(sqlQuery, sqlValues)
            connection.commit()
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return result
    
    @staticmethod
    def set_application_default(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE StoreOwners SET Application_Status = 'Default' WHERE StoreOwnerId = %s"
        sqlValues = (StoreOwnerId,)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    
    @staticmethod
    def set_application_rejected(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "UPDATE StoreApplications SET ApplicationStatus = 'Rejected' WHERE StoreOwnerId = %s"
        sqlValues = (StoreOwnerId,)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result

