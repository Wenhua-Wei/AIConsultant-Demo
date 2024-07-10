from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
load_dotenv('.env')

class Sql:
    def __init__(self,app:Flask):
        app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST") 
        app.config['MYSQL_USER'] = os.getenv("MYSQL_USER") 
        app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD") 
        app.config['MYSQL_DB'] = os.getenv("MYSQL_DB") 
        self.mysql = MySQL(app)

   
    def selectUser(self, telephone:str):
        cur = self.mysql.connection.cursor()
        cur.execute('SELECT * FROM User WHERE telephone = %s', [telephone])
        result=cur.fetchone()
        cur.close()
        return result
    
    def selectAllUsers(self):
        cur=self.mysql.connection.cursor()
        cur.execute('SELECT * FROM User')
        users = cur.fetchall()
        cur.close()
        return users

    def selectCustomers(self):
        cur=self.mysql.connection.cursor()
        cur.execute('SELECT * FROM User where type=0')
        users = cur.fetchall()
        cur.close()
        return users


    def addUser(self,telephone:str,company_name:str,user_type:bool):
        cur = self.mysql.connection.cursor()
        cur.execute('INSERT INTO User (telephone, company_name, type,info_status) values (%s,%s,%s,%s)',(telephone,company_name,user_type,"incompleted"))
        self.mysql.connection.commit()
        cur.close()
        return True
    
    def changeStatus(self,telephone:str):
        cur = self.mysql.connection.cursor()
        cur.execute('UPDATE User SET info_status = %s WHERE telephone = %s',("completed",telephone))
        self.mysql.connection.commit()
        cur.close()
        return True


    def matchTelAndPsw(self, telephone:str,password :str):
        user=self.selectUser(telephone)
        return (False, user)[user.password==password]
   
    
    def isTelephoneExist(self, telephone:str):
        user=self.selectUser(telephone)
        return user
    
    def insertCompanyInfo(self,telephone:str,info:str,app):
        with app.app_context():
            cur = self.mysql.connection.cursor()
            cur.execute('UPDATE User SET company_info = %s WHERE telephone = %s',(info,telephone))
            self.mysql.connection.commit()
            cur.close()
            return True
    
    def getCompanyInfoByTelephone(self, telephone: str):
        cur = self.mysql.connection.cursor()
        # Ensure the column names match your database schema
        cur.execute('SELECT company_info FROM User WHERE telephone = %s', [telephone])
        result = cur.fetchone()
        cur.close()

        # Check if any result is found
        if result:
            # Assuming 'company_info' is the column name where the info is stored
            return result[0]  # Return the company info
        else:
            return None  # Return None if no matching record is found
        
    def supplement(self,telephone:str,name:str,position:str):
        cur = self.mysql.connection.cursor()
        cur.execute('UPDATE User SET name=%s,position=%s where telephone=%s',(name,position,telephone))
        self.mysql.connection.commit()
        cur.close()
        return True
    
    def updateStauts(self,telephone:str,app):
        with app.app_context():
            cur=self.mysql.connection.cursor()
            cur.execute('UPDATE User SET info_status=%s where telephone=%s', ['completed', telephone])
            self.mysql.connection.commit()
            cur.close()
            return True
    
    def isCompleted(self,telephone:str):
        cur=self.mysql.connection.cursor()
        cur.execute('SELECT info_status FROM User WHERE telephone= %s',[telephone])
        result = cur.fetchone()
        self.mysql.connection.commit() 
        cur.close()
        return result[0]=='incompleted'

        