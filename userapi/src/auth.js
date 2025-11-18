import passport from "passport"; // We need this to handle the cookies
import { Strategy } from "passport-local"; // We need this to handle the cookies

import ctrl from "../../managerCtrl/managerController.js"

// The function 'verfiy' inside Strategy is invoked when /login is posted.
// This function checks if the username/ password is correct (or more precisely, passes the data to the manager controller to do so)
// username/ password values are given by the frontend's request object
passport.use( new Strategy( 
    {passReqToCallback : true}, // Access to full req. object
    async function verfiy(req, username, password, cb) {
        
        const unipasskey = req.body.unipasskey

        // Send client 'username' and 'password' to the 'manCtl' subsystem: check if match in the database.
        const validLogin = await ctrl.queryLogin(username, password); // Pass to Manager Controller (invoke corresponding function), wait for result
        const validPasskey = await ctrl.queryPasskey(username, unipasskey) // Check passkey is also valid

        // if there is a match, any request from this user will have two methods added to the 'req' object:
        // "req.isAuthenticated()" (which will be 'true' if login is correct)
        // "req.user" - a method that stores the user's data you pass like {username}, access this with "req.user.username"
        if(validLogin && validPasskey){
            return cb(null, {username: username, passkey: unipasskey});
        }else{
            return cb(null, false);
        }
    }
));

// If login was succesful, create user object
// This function is invoked automatically in Strategy, when "answer" is true
// It tells 'passport' what piece of data we want to save for the user (user object), so with each request, we can access this piece of data
passport.serializeUser((user, cb) => { 
    cb(null, user);
  });

// Retrieves user object for current session
passport.deserializeUser((user, cb) => {
   cb(null, user);
});