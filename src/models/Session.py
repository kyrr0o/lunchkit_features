"""
Session Model
------------

Manages user session storage and lifecycle in the database.
Handles creation, retrieval, and cleanup of session data.


Methods:
    - save_session: Creates or updates session records
    - get_session: Retrieves active session data
    - delete_session: Removes specific session
    - cleanup_expired: Maintenance method for removing stale sessions

"""



from src.database import db_connection
import pymysql.cursors
import json


class Session:
    @staticmethod
    def save_session(session_id,user_data,expires_at,ip_address,user_agent):
        connection = db_connection()
        cursor = connection.cursor()
        sqlQuery = """
            INSERT INTO sessions (id, user_data, expires_at, ip_address, user_agent) 
            VALUES (%s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE 
                user_data = VALUES(user_data),
                expires_at = VALUES(expires_at)
        """
        sqlValues = (session_id, json.dumps(user_data), expires_at, ip_address, user_agent)
        cursor.execute(sqlQuery, sqlValues)
        connection.commit()
        cursor.close()
        connection.close()


    @staticmethod
    def get_session(session_id):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT * FROM sessions WHERE id = %s "
        sqlValues = (session_id,)
        cursor.execute(sqlQuery, sqlValues)
        session = cursor.fetchone()
        cursor.close()
        connection.close()
        return session
    
    @staticmethod
    def delete_session(session_id):
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
        connection.commit()
        connection.close()

    @staticmethod
    def cleanup_expired():
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sessions WHERE expires_at < NOW()")
        connection.commit()
        connection.close()