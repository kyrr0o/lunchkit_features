"""
Application Document Model Module
-------------------------------

This module handles database operations for store registration documents,
providing methods for storing and managing document URLs.

Key Components:
    - Database operations for registration documents
    - Document URL storage handling
    - Application document linking

Methods:
    - create_applicationDocument: Store document URLs for application
        * Links documents to store application ID
        * Stores URLs for all required permits and certificates
        * Handles database connection and cleanup
        
"""


from src.database import db_connection
import pymysql.cursors

class ApplicationDocument:
    @staticmethod
    def create_applicationDocument(StoreApplicationId,SanitaryPermit,CertificateOfBusinessNameRegistration,BusinessPermit,FireSafetyInspectionCertificate,CertificateOfRegistration,TaxPaymentForm):
        connection = db_connection()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        SqlQuery = "INSERT INTO ApplicationDocuments (StoreApplicationId,SanitaryPermit,CertificateOfBusinessNameRegistration,BusinessPermit,FireSafetyInspectionCertificate,CertificateOfRegistration,TaxPaymentForm) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        sqlValues = (StoreApplicationId,SanitaryPermit,CertificateOfBusinessNameRegistration,BusinessPermit,FireSafetyInspectionCertificate,CertificateOfRegistration,TaxPaymentForm)
        cursor.execute(SqlQuery,sqlValues)
        connection.commit()
        cursor.close()
        connection.close()


