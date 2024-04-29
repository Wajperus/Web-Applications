#!C:\Users\Korisnik\AppData\Local\Programs\Python\Python310\python.exe

import db
import os
import hashlib
import cgi
form=cgi.FieldStorage()

print("Content-type: text/html\n")
print()

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
    <form action="vjezba3main.py" method="POST">
          <table>
            <tr>
                <td>Ime:</td>
                <td><input type="text" name="ime2"></td>
            </tr>
            <tr>
                <td>Lozinka:</td>
                <td><input type="password" name="lozinka3"></td>
            </tr>
          </table>
          <input type="submit" value="Prijavi se">
    </form>
    </body>
          </html>
     """)


html_started=False

###### PROVJER ZA REGISTRACIJU ######


def hash_password(password):
    password_bin = password.encode('utf-8')
    salt = os.urandom(32)
    hash = hashlib.pbkdf2_hmac(
        'sha256', password_bin, salt, 100000
    )
    return salt + hash

lozinka=form.getvalue("lozinka")
lozinka2=form.getvalue("lozinka2")


    

def verify_password(password_plain_text, stored_password_hash):
    salt = stored_password_hash[:32]
    key = stored_password_hash[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', password_plain_text.encode('utf-8'), salt, 100000)
    return (key == new_hash)

if lozinka is not None and lozinka2 is not None:
    lozinka=hash_password(lozinka)
    if not db.chech_username_exists(form.getvalue("ime")) and not db.chech_email_exists(form.getvalue("email")):
        if verify_password(lozinka2, lozinka):
            db.insert_user(form.getvalue("ime"), form.getvalue("email"), lozinka)
            print("Content-type: text/html")
            print()
            start_html()
            html_started=True
        else:
            print("Status: 302 Moved")
            print("Content-type: text/html")
            print("Location: forma_registracija.py?error=Lozinke se ne podudaraju")
            print()  # end of headers
    else:
        print("Status: 302 Moved")
        print("Content-type: text/html")
        print("Location: forma_registracija.py?error=Korisnik vec postoji")
        print()  # end of headers

if not html_started:
    start_html()