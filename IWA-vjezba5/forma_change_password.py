#!C:\Users\Korisnik\AppData\Local\Programs\Python\Python310\python.exe

import db
import session
import cgi
import hashlib
import os
import traceback

form=cgi.FieldStorage()


# print("Location: forma_login.py")
# print()

if "error" in form:
    print(form.getvalue("error"))

def start_html():
    print("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
          table th,td{
            border-style: solid;
          }
    </style>
    </head>
    <body>
    <form action="forma_change_password.py" method="POST">
          <table>
            <tr>
                <td>Unesite Staru Lozinku:</td>
                <td><input type="password" name="lozinka4"></td>
            </tr>
            <tr>
                <td>Unesite Novu Lozinku:</td>
                <td><input type="password" name="lozinka5"></td>
            </tr>
            <tr>
                <td>Ponovite Lozinku:</td>
                <td><input type="password" name="lozinka6"></td>
            </tr>
          </table>
          <input type="submit" value="Potvrdi">
    </form>
    </body>
          </html>
     """)

#start_html()


html_started=False

########## DOHVACANJE LOZINKE ZA TOG KORISNIKA #########


session_id=session.get_or_create_session_id()

_, data=db.get_session(session_id)



lozinka4=form.getvalue("lozinka4")
lozinka5=form.getvalue("lozinka5")
lozinka6=form.getvalue("lozinka6")
ime=data.get('ime2')
#print(ime)
old_password=db.get_password(ime)

#print(old_password)

def hash_password(password):
    password_bin = password.encode('utf-8')
    salt = os.urandom(32)
    hash = hashlib.pbkdf2_hmac(
        'sha256', password_bin, salt, 100000
    )
    return salt + hash

def verify_password(password_plain_text, stored_password_hash):
    salt = stored_password_hash[:32]
    key = stored_password_hash[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', password_plain_text.encode('utf-8'), salt, 100000)
    return (key == new_hash)

if lozinka4 is not None and verify_password(lozinka4, old_password)==False:
    print("Content-type: text/html\n")
    print("Unijeli ste neispravnu staru lozinku!")
    #print("Location: http://localhost/cgi-bin/IWA-vjezba5/forma_change_password.py?error+Niste+unijeli+ispravnu+staru+lozinku")
    print()
    #start_html()
    #html_started=True

if lozinka5 is not None and lozinka5==lozinka6:
    new_password=hash_password(lozinka5)
    db.update_password(data.get('user_id'), new_password)
    print("Location: http://localhost/cgi-bin/IWA-vjezba5/forma_login.py")
    print()


#if not html_started:
  
start_html()























