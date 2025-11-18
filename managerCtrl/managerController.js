import axios from "axios"
import openAiAPI from "../openaiApi/chatgpt.js"
import fs from "fs"

function queryLogin(email, password){
    return axios.post("http://localhost:8000/queryLogin", { "email": email, "password" : password })
    .then( (res) => {
        return res.data.result; // Boolean value
    })
    .catch( (error)=>{
        console.log(error)
        return false
    })
}

function queryPasskey(email, passkey){
    return axios.post("http://localhost:8000/queryPasskey", { "email": email, "passkey" : passkey })
    .then( (res)=> {
        return res.data.result; // Boolean value
    })
    .catch( (error)=>{
        console.log(error)
        return false
    })
}

function querySignupStudent(email, password, passkey){
    return axios.post("http://localhost:8000/querySignupStudent", {"email": email, "password": password, "passkey": passkey})
    .then( (res) => {
        const emailUnused = res.data.emailUnused
        const validPasskey = res.data.validPasskey // University must already exist

        // Account has been created in app.py
        if (validPasskey && emailUnused){
            return true
        }
        return false
    })
    .catch( (error)=>{
        console.log(error)
        return false
    })
}

// Retrieves module curriculum & merges to one file
// Sends file to openAI API
function generateExam (_module){
    return axios.post("http://localhost:8000/queryModuleCurriculum", {"module": _module}, {responseType: "arraybuffer"})
    .then( async (res) => {
        fs.writeFileSync("retrievedCurriculum.pdf", res.data) // Retrieves merged curriculum
        const examMarkown = await openAiAPI.generateExam("./retrievedCurriculum.pdf") // Send written curriculum to openai, store response
        return examMarkown        
    })
    .catch( (error) => {
        console.log(error)
    })
}

export default {
    queryLogin,
    queryPasskey,
    querySignupStudent,
    generateExam
}