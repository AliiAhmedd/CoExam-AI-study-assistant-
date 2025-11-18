# Entry point for starting the python server
# Python server is run locally: not hosted
# Uses flask to handle incoming Requests
# Manager Controller POSTS these functions
# These functions are just an internal API: they are required to invoke the actual security logic to get a response

# import threading
import flask
import crypto
import queries
import PyPDF2 #we need this library to merge the pdf files into one single file.

app = flask.Flask(__name__)
# this server act like a bridge btw the managgerController and python security subsystem and database***

@app.route("/queryLogin", methods=["POST"])
def queryLogin():
    # Get username, password from Manager Controller (sent as JSON object):
    obj = flask.request.get_json() # Get JSON from manager controller
    email = obj.get("email") # Extract values from keys
    password = obj.get("password")

    result = False

    storedHash = queries.query_retriving_password(email)
    if storedHash is not None:
        result = crypto.check_password(password, storedHash)
    
    return flask.jsonify({"result": result})

@app.route("/queryPasskey", methods=["POST"])
def queryPasskey():

    obj = flask.request.get_json() 
    email = obj.get("email")
    passkey = obj.get("passkey")

    result = False

    storedPasskey = queries.query_retrieving_user_passkey(email)
    if crypto.check_password(passkey, storedPasskey):
        result = True

    return flask.jsonify({"result": result})


@app.route("/querySignupStudent", methods=["POST"])
def query_singup_student():

    obj = flask.request.get_json() 
    email = obj.get("email")
    password = obj.get("password")
    passkey = obj.get("passkey") 

    emailUnused = False
    validPasskey = False

    # Check if email already exists
    email = queries.query_email(email)
    if email is None:
        emailUnused: True

    # Check if passkey belongs to a university & return university name
    # Encode passkey to bytes
    passkeyBytes = passkey.encode("utf-8")
    uniname = queries.query_retriving_uni_name(passkeyBytes)

    # No uni - Wrong passkey
    if uniname is None:
        validPasskey = False

    if emailUnused and validPasskey:
        hashedPassword = crypto.hash_plaintext(password)
        queries.query_adding_new_student(email, hashedPassword, uniname)

    return flask.jsonify({"emailUnused": emailUnused, "validPasskey" : validPasskey})

#this function is going to reterive all the curriculm slides and past paper in the DB for the given module name and universy. Then it is going to merge them into one pdf file. Then it is going to send this file to the manager controller.
@app.route("/queryModuleCurriculum", methods=["POST"])
def query_module_curriculm_and_past_paper():

    obj = flask.request.get_json() 
    module_name = obj.get("module")

    pdf_files_curriculm = queries.query_retriving_curriculum(module_name)#these pdf files are wrapped in ByteIO object 
    pdf_files_past_paper = queries.query_retriving_past_paper(module_name)#these pdf files are wrapped in ByteIO object 

    merger = PyPDF2.PdfWriter()

    if pdf_files_curriculm is not None:
        for pdf in pdf_files_curriculm:
            merger.append(pdf)

    if pdf_files_past_paper is not None:
        for pdf in pdf_files_past_paper:
            merger.append(pdf)
        
    # If no curriculum written to merger, this file is a zero-page PDF
    merger.write("mergedCurriculum.pdf")
    merger.close()

    return flask.send_file(
        "mergedCurriculum.pdf",
        as_attachment=False,
        mimetype="application/pdf" # Sends file as binary
    )

if __name__ == "__main__":
    app.run(host="localhost", port=8000)
