import mysql.connector
from io import BytesIO #we need this to wrap the PDF into ByteIO object and then send it to the server(app.py)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = "CoExamDatabase"
)

cursor = connection.cursor()

# Checks if email exists
def query_retrieving_email(email):
    
    query = "SELECT email FROM Student WHERE email = %s"
    cursor.execute(query, (email,))
    email = cursor.fetchone()

    return email

#this query is going to return the hashed password of the user with its salt.
def query_retriving_password(email):

    query = "SELECT password FROM Student WHERE email = %s"
    cursor.execute(query, (email,))
    password = cursor.fetchone()

    if password:
        return password[0]
    return None

def query_retrieving_user_passkey(email):
    query = "SELECT passkey FROM Student WHERE email = %s"
    cursor.execute(query, (email,))
    passkey = cursor.fetchone()

    if passkey:
        return passkey[0]
    return None

def query_retriving_user_uni(email):

    query = "SELECT uni FROM Student WHERE email = %s"
    cursor.execute(query, (email,))
    uni_name = cursor.fetchone()

    if uni_name:
        return uni_name[0]
    return None

def query_retriving_uni_passkey(university_name):

    query = "SELECT passkey FROM University WHERE uniName = %s "
    cursor.execute(query, (university_name,))
    passkey = cursor.fetchone()

    if passkey:
        return passkey[0]
    return None

# Retrieve the university, given a passkey
def query_retriving_uni_name(passkey):

    query = "SELECT uniName FROM University WHERE passkey = %s "
    cursor.execute(query, (passkey,))
    uniname = cursor.fetchone()

    if uniname:
        return uniname[0]
    return None

#this query is going to retrive all the module names that the given uni has uploaded curriculum for
def query_modules_with_curriculum(university_name):
    
    query = "SELECT moduleName FROM Curriculum WHERE uni = %s"
    cursor.execute(query, (university_name,))
    module_names = cursor.fetchall()

    return module_names

#the return curriculum is going to be bytes-like object.
def query_retriving_curriculum(module_name):
    query = "SELECT content FROM Curriculum WHERE moduleName = %s"
    cursor.execute(query, (module_name,))
    curriculum = cursor.fetchall()

    if curriculum is not None:
        pdf_list = []

        for binary_pdf in curriculum:
            pdf_list.append( BytesIO(binary_pdf[0]) )

        # print(pdf_list)
    return pdf_list


def query_retriving_past_paper(module_name):

    query = "SELECT content FROM PastPaper WHERE moduleName = %s"
    cursor.execute(query, (module_name,))
    past_papers = cursor.fetchall()

    if past_papers is not None:
        pdf_list = []

        for binary_pdf in past_papers:
            pdf_list.append( BytesIO(binary_pdf[0]) )

        # print(pdf_list)
    return pdf_list

#the return list of generated past paper are going to be pdf file.
def query_retriving_generated_past_paper(university_name, module_name):

    query = "SELECT content FROM GeneratedPastPaper WHERE uni = %s AND moduleName = %s"
    cursor.execute(query, (university_name,module_name,))
    generated_past_papers = cursor.fetchall()

    pdf_list = []

    for binary_pdf in generated_past_papers:
        pdf_list.append( BytesIO(binary_pdf[0]) )

    return pdf_list

def query_adding_new_university(uni_name, password, passkey):

    query = "INSERT INTO University(uniName, password, passkey) VALUES(%s, %s, %s)"
    cursor.execute(query, (uni_name, password, passkey))
    connection.commit()

def query_adding_new_student(email, password, passkey, university_name):

    query = "INSERT INTO Student(email, password, passkey, uni) VALUES(%s, %s, %s, %s)"
    cursor.execute(query, (email, password, passkey, university_name))
    connection.commit()

# this function expect the argument 'content' to be binary data.
def query_adding_curriculum(content, module_name):

    query = "INSERT INTO Curriculum(content, moduleName) VALUES(%s, %s)"
    cursor.execute(query, (content,module_name))
    connection.commit()

# this function expect the argument 'content' to be binary data.
def query_adding_past_paper(content, module_name):

    query = "INSERT INTO PastPaper(content, moduleName, uni) VALUES(%s, %s)"
    cursor.execute(query, (content,module_name))
    connection.commit()

# this function expect the argument 'content' to be binary data.
def query_adding_generated_past_paper(content, module_name):

    query = "INSERT INTO GeneratedPastPaper(content, moduleName, uni) VALUES(%s, %s)"
    cursor.execute(query, (content,module_name))
    connection.commit()
