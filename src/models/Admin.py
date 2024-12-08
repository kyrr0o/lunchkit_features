from src.database import db_connection
import pymysql.cursors

class Admin:

   
    @staticmethod
    def get_admin(Email):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        SqlQuery = "SELECT * FROM Admins WHERE Email = %s"
        SqlValues = (Email,)
        cursor.execute(SqlQuery, SqlValues)
        admin = cursor.fetchone()
        cursor.close()
        connection.close()
        return admin