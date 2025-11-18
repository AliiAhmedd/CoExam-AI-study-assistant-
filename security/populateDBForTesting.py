# To use this file, ensure the database already exists AND you have the PDFs to upload with the correct name, in this directory

import mysql.connector

import queries
import crypto

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = "CoExamDatabase"
)

cursor = connection.cursor()

def main():

    # Variables for queries
    uniName = "LancasterUni"
    password = crypto.hash_plaintext("lancsPass")

    studentEmail = "someExample@example.com"
    studentPassword = crypto.hash_plaintext("myPass")
    passkey = crypto.hash_plaintext("1234")
    
    moduleName = "scc221"

    # Populate Curriculum with two lecture PDF entries (211)
    with open("lecture1.pdf", "rb") as file:
        lecture1_bytes = file.read()

    with open("lecture2.pdf", "rb") as file:
        lecture2_bytes = file.read()

    # with open("past_paper1.pdf", "rb") as file:
    #     past_paper1_bytes = file.read()


    queries.query_adding_new_university(uniName, password, passkey)

    queries.query_adding_new_student(studentEmail, studentPassword, passkey, uniName)

    queries.query_adding_curriculum(lecture1_bytes, moduleName)

    queries.query_adding_curriculum(lecture2_bytes, moduleName)

    # queries.query_adding_past_paper(past_paper1_bytes, moduleName)

    connection.commit()

if __name__ == "__main__":
    main()