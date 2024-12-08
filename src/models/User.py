"""
User Model
---------

Handles all user-related database operations using PyMySQL.
Manages user creation, retrieval, and updates in the system.



Methods:
    - create_user: Creates new user entry
    - get_user_by_google_id: Retrieves user by Google ID
    - update_user: Updates existing user information


"""
from src.database import db_connection
import pymysql.cursors

class User:

    @staticmethod
    def create_user(google_id,username,email):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)     
        sqlQuery = "INSERT INTO USERS (google_id,username,email) VALUES (%s,%s,%s)"
        sqlValues = (google_id,username,email)
        cursor.execute(sqlQuery,sqlValues)
        connection.commit()
        cursor.close()
        connection.close()
        return User.get_user_by_google_id(google_id)
    
    @staticmethod
    def get_user_by_google_id(google_id):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM USERS WHERE google_id = %s"
        sqlValues = (google_id,)
        cursor.execute(sqlQuery,sqlValues)
        user = cursor.fetchone()
        connection.close()
        return user
    
    @staticmethod
    def update_user(username,google_id):
        connection = db_connection()
        cursor = connection.cursor()
        sqlQuery = "UPDATE USERS SET username = %s where google_id = %s"
        sqlValues = (username,google_id)
        cursor.execute(sqlQuery,sqlValues)
        connection.commit()
        cursor.close()
        connection.close()
        return User.get_user_by_google_id(google_id)
