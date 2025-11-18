// Class used as entry point for backend. Has three purposes:
// 1. Starts the server 
// 2. Serves client static files (../..frontend/public) when a request is made to the domain (client entry point)
// 3. Forwards any API requests directly to ../routes/endpoints.js when a request is made, to handle that request 

import express from "express"; //we need this to makes this script as server that is going to take request from the client and the frontend
import session from "express-session"; // we need this to handle the cookies
import passport from "passport"; // we need this to handle the cookies
import cookieParser from "cookie-parser" // Required to read cookies from requests


//we need these to slve the problems that comes with the path of files we are going to send to the user
import path, { dirname } from "path";
import { fileURLToPath } from "url";

import "./auth.js";
import endpoints from "./endpoints.js"

// This solves the problems that comes with the path of files we are going to send to the user
const __dirname = dirname(fileURLToPath(import.meta.url));


const app = express();

// URL encoded parser for requests
app.use(express.urlencoded({ extended: false }));
app.use(express.json())
app.use(cookieParser())

app.use(session({
    secret:"this should be a string that represents the key for encrypting the cookies",//this should comes from env file.
    resave: false,
    saveUninitialized:true,
    cookie: { maxAge: 1000*60*60*24 } //this is the time for preserving the session in miliseconds
}))

app.use(passport.initialize());
app.use(passport.session());

// Any request will be forwarded to the endpoint class for routing handling
app.use(endpoints)

// Serve the public static files to user (images, css, JS) 
// Requires absoloute path (__dirname) of server.js. Is concatanted with relative frontend/public
app.use(express.static(path.join(__dirname, '../../../frontend/public')))

app.listen(5000, () => console.log("Server running on port 5000")) // Starts the server on port 5000