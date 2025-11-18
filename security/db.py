# Script to initialise the database
# This script is only to be executed once to initialise the database during first setup.
import mysql.connector

# Connect to the local MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = connection.cursor()

# Count existing databases
cursor.execute("SHOW DATABASES")

number_of_databases = 0

for i in cursor.fetchall():
    number_of_databases +=1

# MySQL has 4 built-in default databases, if only those exist, our database hasn't been created yet.
if( number_of_databases == 4):
    # Create the application database
    cursor.execute("CREATE DATABASE CoExamDatabase")

    cursor.execute("USE CoExamDatabase")

    # Creating the tables
    cursor.execute("CREATE TABLE University( uniName VARCHAR(100) PRIMARY KEY, password VARCHAR(255) NOT NULL, passkey VARCHAR(255) NOT NULL)")
    cursor.execute("CREATE TABLE Student( email VARCHAR(100) PRIMARY KEY, password VARCHAR(255) NOT NULL, passkey VARCHAR(255) NOT NULL, uni VARCHAR(100) NOT NULL, FOREIGN KEY(uni) REFERENCES University(uniName) )")
    cursor.execute("CREATE TABLE Curriculum( content LONGBLOB NOT NULL, moduleName VARCHAR(255), uni VARCHAR(100), FOREIGN KEY(uni) REFERENCES University(uniName) )")
    cursor.execute("CREATE TABLE PastPaper( content LONGBLOB NOT NULL, moduleName VARCHAR(255) NOT NULL,  uni VARCHAR(100), FOREIGN KEY (uni) REFERENCES University(uniName) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE GeneratedPastPaper( content LONGBLOB NOT NULL, moduleName VARCHAR(255) NOT NULL, uni VARCHAR(100), FOREIGN KEY (uni) REFERENCES University(uniName) ON DELETE CASCADE)")
