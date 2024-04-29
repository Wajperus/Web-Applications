#!C:\Users\Korisnik\AppData\Local\Programs\Python\Python310\python.exe

import cgi

form=cgi.FieldStorage()

print("Content-type: text/html\n")

if "error" in form:
    print(form.getvalue("error"))

def start_html():
    #print("Content-type: text/html\n")
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
    <form action="forma_login.py" method="POST">
          <table>
            <tr>
                <td>Ime:</td>
                <td><input type="text" name="ime"></td>
            </tr>
            <tr>
                <td>Email:</td>
                <td><input type="email" name="email"></td>
            </tr>
            <tr>
                <td>Lozinka:</td>
                <td><input type="password" name="lozinka"></td>
            </tr>
            <tr>
                <td>Ponovite lozinku:</td>
                <td><input type="password" name="lozinka2"></td>
            </tr>
          </table>
          <input type="submit" value="Registriraj se">
    </form>
    </body>
          </html>
     """)
    
start_html()
