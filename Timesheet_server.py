import mysql.connector
from mysql.connector import Error
import pandas as pd

result = []

def create_connection(host_name,user_name,password): #creating server connection
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = password
        )
        print("database connection was successful")
    except Error as err:
        print(f"error: '{err}'")
    
    return connection

def create_db_connection(host_name,user_name,password,db_name): # creates connection to the database
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = password,
            database = db_name
        )
    except Error as err:
        print(f"error: '{err}'")
    
    return connection

def create_database(connection,query): #creating the actual database
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("database is created successfully")
    except Error as err:
        print(f"error: '{err}'")

def execute_query(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("query is executed successfully.")
    except Error as err:
        print(f"error: '{err}'")

def Insert_login_query(connection,query,primary_key,id,pw):
    cursor = connection.cursor()
    try:
        cursor.execute(query,(primary_key,id,pw))
        connection.commit()
        print("Insert query is executed successfully.")
    except Error as err:
        print(f"error: '{err}'")

def Insert_user_query(connection,query,Date,Hours,Note,user_name,Travel_status):
    cursor = connection.cursor()
    try:
        cursor.execute(query,(Date,Hours,Note,Travel_status,user_name,Date))
        connection.commit()
        print("This should be running when I'm updating the values with the condition of existing date.")
    except Error as err:
        print(f"error: '{err}'")
def Insert_user_info_query(connection,query,username,Date,Hours,Travel_status,Note):
    cursor = connection.cursor()
    try:
        cursor.execute(query,(username,Date,Hours,Travel_status,Note))
        connection.commit()
        print("This should be running when I'm updating Null values.")
    except Error as err:
        print(f"error: '{err}'")
def update_user_info_query1(connection,query,user_name,Date,Hours,Note):
    cursor = connection.cursor()
    try:
        cursor.execute(query,(user_name,Date,Hours,Note))
        connection.commit()
        print("Insert query is executed successfully.")
    except Error as err:
        print(f"error: '{err}'")
def delete_user_info_query(connection,query,Date):
    cursor = connection.cursor()
    try:
        cursor.execute(query,(Date))
        connection.commit()
        print("Delete query is successfully executed.")
    except Error as err:
        print(f"error: '{err}'")
        
def data_fetching(connection,query):
    global result
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
    except Error as err:
        print(f"error: '{err}'")

def user_name_filtering(connection,query,user_name):
    global result
    cursor = connection.cursor()
    try:
        cursor.execute(query,(user_name))
        result = cursor.fetchall()
        connection.commit()
    except Error as err:
        print(f"error: '{err}'")

def Filtering_Dates(connection,query,Date):
    global result
    cursor = connection.cursor()
    try:
        cursor.execute(query,Date)
        result = cursor.fetchall()
        connection.commit()
    except Error as err:
        print(f"error: '{err}'")

create_database_query = "CREATE DATABASE Timesheet_db"
create_login_table_query = """CREATE TABLE Login_Info(
login_id INT PRIMARY KEY,
user_name VARCHAR(40) NOT NULL,
password VARCHAR(40) NOT NULL
)"""
create_user_table_query = """CREATE TABLE User_Info(
user_name VARCHAR(40) NOT NULL,
Date VARCHAR(40),
Hours VARCHAR(20),
Travel VARCHAR(20),
Notes VARCHAR(200)
)""" 