// Class used to listen for requests from the frontend
// Any API call is forwarded here from server.js

// With each request that is received by endpoint, the request object 'req' will have two additional attributes: 
// 'req.user' (for the username), and a method 'req.isAuthenticated()', which should return 'true' if the logging in of this client is correct (used in checkAuth).

import express from "express"; //we need this to makes this script as server that is going to take request from the client and the frontend
import passport from "passport"; // we need this to handle the cookies
import path, { dirname } from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs'
import markdownit from "markdown-it";
import * as pdf from "html-pdf-node";
import ctrl from "../../managerCtrl/managerController.js"

const router = express.Router()
const __dirname = dirname(fileURLToPath(import.meta.url));

// Ensures unexpected requests to endpoints /home are authenticated, else, redirect to login
function checkAuth(req, res, next) {
    if (req.isAuthenticated()) return next();
    res.redirect("/login");
  }

// Unprotected API endpoints (no-auth required) //

// Top-level redirects to login
router.get("/", (req, res) => {
    res.redirect("/login")
})

// Get request serves login page
router.get("/login", (req, res) => {
    res.sendFile(path.join(__dirname + "../../../../frontend/loginpage.html"))
})

// Invokes passport authentication: username/ password extracted from req object
// Verify function (in auth.js) checks if correct: cb (callback function) determines whether redirect is successful or not
router.post('/login', passport.authenticate("local", {
    successRedirect: "/home", // To home page
    failureRedirect: "/login" // Refresh page
    })
);

router.get("/signup", (req, res) => {
    res.sendFile(path.join(__dirname + "../../../../frontend/signup.html"))
})

router.post("/signup", async (req, res) => {
    const {email, password, passkey} = req.body
    const accountCreated = await ctrl.makeAccount(email, password, passkey)
    // If response is true, redirect to login
    if (accountCreated){
        res.redirect('/login')
    }
    else{
        res.redirect('/signup')
    }
})

// Protected API endpoints //

router.get("/home" , checkAuth, (req, res)=>{
    res.cookie("unipasskey", req.user.passkey, {maxAge: 15 * 60 * 1000}) // Stores the given passkey as a cookie for that user, assuming login was successful
    res.sendFile(path.join(__dirname + "../../../../frontend/homepage.html"))
})

router.get("/examgen", checkAuth, (req, res) => {
    res.sendFile(path.join(__dirname + "../../../../frontend/examgen.html"))
})

router.post("/examgen", checkAuth, async (req, res) => {
    const _module = req.body.module
    const outputPath = path.join(__dirname, "generatedExam.pdf");

    const examMarkdown = await ctrl.generateExam(_module)

    // Generate HTML from Markdown
    const md = markdownit()
    const htmlMarkdown = md.render(examMarkdown);

    // Generate PDF from Markdown HTML and send to user
    await pdf.generatePdf({ content: htmlMarkdown}, { format: "A4", path: outputPath });
    res.download(outputPath)
})

// Expose router for server.js to forward requests here
export default router