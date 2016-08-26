import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup Page</title>
    <style type="text/css">
        .error {
            color: red;
            font-weight:bold;
        }
    </style>
</head>
<body>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    # Handles requests coming in to '/'

    def get(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        form_start = """<h1>Signup</h1>
            <table>
            <form action="/welcome" method="post">"""
        table_row_start = "<tr>"
        table_row_end = "</tr>"

        form_username = """<label><td>Username</td>
            <td><input type="text" name="username" value="{}"/></td></label>""".format(username)
        form_username_error = """<td></td>"""

        form_password = """<label><td>Password</td>
            <td><input type="password" name="password" value="{}"/></td></label>""".format(password)
        form_password_error = """<td></td>"""

        form_verify = """<label><td>Verify Password</td>
            <td><input type="password" name="verify" value="{}"/></td></label>""".format(verify)
        form_verify_error = """<td class="error"></td>"""

        form_email = """<label><td>Email (optional)</td>
                    <td><input type="text" name="email" value="{}"/></td></label>""".format(email)
        form_email_error = """<td class="error"></td>"""

        form_end = """<tr><td></td><td><input type="submit"/></td></tr>
            </form>
            </table>
        """

        # combine all the pieces to build the content of our response
        message = ""

        error = self.request.get("error")
        if error == "username":
            form_username_error = "<td class='error'>Invalid username</td>"
        elif error == "password":
            form_password_error = "<td class='error'>Invalid password</td>"
        elif error == "verify":
            form_verify_error = "<td class='error'>Does not match</td>"
        elif error == "email":
            form_email_error = "<td class='error'>Invalid email</td>"

        response = page_header + form_start
        response += table_row_start + form_username + form_username_error + table_row_end
        response += table_row_start + form_password + form_password_error + table_row_end
        response += table_row_start + form_verify + form_verify_error + table_row_end
        response += table_row_start + form_email + form_email_error + table_row_end
        response += form_end + page_footer

        self.response.write(response)

class Signup(webapp2.RequestHandler):
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        #params = dict(username = username,
        #              email = email)

        if not valid_username(username):
            error = "username"
            error_message = "<p class='error'>That's not a valid username.</p>"
            have_error = True

        if not valid_password(password):
            error = "password"
            error_message = "<p class='error'>That wasn't a valid password.</p>"
            have_error = True
        elif password != verify:
            error = "verify"
            error_message = "<p class='error'>Your passwords didn't match.</p>"
            have_error = True

        if not valid_email(email):
            error = "email"
            error_message = "<p class='error'>That's not a valid email.</p>"
            have_error = True

        if have_error:
            self.redirect("/?error=" + error + "&username=" + username +
                "&password=" + password + "&verify=" + verify + "&email=" + email)
        else:
            welcome = "<h1>Welcome, " + username + "!</h1>"

            self.response.write(page_header + welcome + page_footer)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Signup)
], debug=True)
