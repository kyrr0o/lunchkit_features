"""

Store Application Model Module
----------------------------

This module handles database operations for store applications, providing
methods for creating and managing application records.

Key Components:
    - Database CRUD operations for applications
    - Application status tracking
    - Document relationship management

Methods:
    - create_storeApplication: Create new store application record
    - search_storeApplication: Find application by ID
    - get_storeApplicationWithDocuments: Retrieve complete application data


"""

from src.database import db_connection
import pymysql.cursors

class StoreApplication:
    @staticmethod
    def create_storeApplication(StoreApplicationId,StoreOwnerId,StoreName,ApplicationStatus):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        SqlQuery = "INSERT INTO StoreApplications (StoreApplicationId,StoreOwnerId,StoreName,ApplicationStatus) VALUES (%s,%s,%s,%s)"
        sqlValues = (StoreApplicationId,StoreOwnerId,StoreName,ApplicationStatus)
        cursor.execute(SqlQuery,sqlValues)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def search_storeApplication(StoreApplicationId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreApplications WHERE StoreApplicationId = %s"
        sqlValues = (StoreApplicationId,)
        cursor.execute(sqlQuery,sqlValues)
        owner = cursor.fetchone()
        cursor.close()
        connection.close()
        return owner
    
    @staticmethod
    def get_storeApplicationWithDocuments():
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM StoreApplications S JOIN ApplicationDocuments A on S.StoreApplicationId = A.StoreApplicationId")
        completeApplications = cursor.fetchall()
        cursor.close()
        connection.close()
        return completeApplications
        
    @staticmethod
    def get_approved_store_application(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreApplications WHERE StoreOwnerId = %s AND ApplicationStatus = 'Approved'"
        sqlValues = (StoreOwnerId,)
        cursor.execute(sqlQuery, sqlValues)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    
    @staticmethod
    def getLatestApplication(StoreOwnerId):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM StoreApplications Where StoreOwnerId = %s ORDER BY SubmissionDate DESC LIMIT 1"
        sqlValue = (StoreOwnerId,)
        cursor.execute(sqlQuery,sqlValue)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result