#!C:\Users\Korisnik\AppData\Local\Programs\Python\Python310\python.exe

import db
import session
from http import cookies

session_id = session.get_or_create_session_id()


db.destroy_session(session_id)


def delete_cookie():
    cookie = cookies.SimpleCookie()
    cookie['session_id'] = ""
    cookie['session_id']['expires'] = 0
    print(cookie.output())

delete_cookie()

print("Location: http://localhost/cgi-bin/IWA-vjezba5/forma_login.py")
print()