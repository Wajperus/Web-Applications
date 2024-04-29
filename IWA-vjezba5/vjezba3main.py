#!C:\Users\Korisnik\AppData\Local\Programs\Python\Python310\python.exe


import base, podaci
import session
import db
import cgi
import hashlib
form=cgi.FieldStorage()

# print("Content-type: text/html\n")
# print()

ime2=form.getvalue("ime2")
lozinka3=form.getvalue("lozinka3")
old_hashed_password=db.get_password(ime2)

if(form.getvalue("key")=="Logout"):
    print("Status: 302 Moved")
    print("Location: http://localhost/cgi-bin/IWA-vjezba5/forma_logout.py")
    print()
    exit(0)

if(form.getvalue("key")=="Change Password"):
    print("Status: 302 Moved")
    print("Location: http://localhost/cgi-bin/IWA-vjezba5/forma_change_password.py")
    print()
    exit(0)
    
hash_password = db.get_password(ime2)

def verify_password(password_plain_text, stored_password_hash):
    if stored_password_hash is None:
        return False
    salt = stored_password_hash[:32]
    key = stored_password_hash[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', password_plain_text.encode('utf-8'), salt, 100000)
    return (key == new_hash)

# Dohvatite trenutnu sesiju ili stvorite novu
session_id = session.get_or_create_session_id()

# Dohvatite podatke sesije
_, data = db.get_session(session_id)

if verify_password(lozinka3, hash_password):
    # Pretpostavljamo da imate funkciju koja može dohvatiti user_id koristeći ime2
    user_id = db.get_user_id(ime2)

    # Dodajte user_id u podatke sesije
    data['user_id'] = user_id
    data['ime2'] = ime2
    #data['lozinka3'] = old_hashed_password

    # # Zamijenite trenutne podatke sesije s novim podacima
    db.replace_session(session_id, data)
    print("Content-type: text/html")
    print()
    print("Hej " + db.get_name(user_id) + " !")
else:
    # Provjerite postoji li user_id u podacima sesije
    if 'user_id' not in data:
        # Ako ne postoji, preusmjerite korisnika na stranicu za prijavu
        print("Location: http://localhost/cgi-bin/IWA-vjezba5/forma_login.py?error=Neispravna lozinka ili korisnicko ime")
        print()
        exit(0)

db.replace_session(session_id, data)
################# SESSION #################

seleceted_year=None
if "key" in form:
    seleceted_year=podaci.year_ids[form.getvalue("key")]

def print_prvi_red():
    print("""<tr>
          <th>Subject</th>
          <th>Status</th>
          <th>ECTS</th>
          </tr>""")

def printaj_imena(seleceted_year):
     session_id=session.get_or_create_session_id()
     _, data=db.get_session(session_id)
     for key in podaci.subjects:
        if podaci.subjects[key]['year']==seleceted_year:
            status=data.get(key, "Ne upisuje")
            print("""
                  <tr>
                  <td>"""+ podaci.subjects[key]['name']+ """</td>
                  <td>
                    <input type="radio" name="""+key+""" value="Ne upsiuje" """ + ("checked" if status == "Ne upisuje" else "") + """>Ne upisuje
                    <input type="radio" name="""+key+""" value="Upisuje" """ + ("checked" if status == "Upisuje" else "") + """>Upisuje
                    <input type="radio" name="""+key+""" value="Polozen" """ + ("checked" if status == "Polozen" else "") + """>Polozen
                  </td>
                  <td>""" + str(podaci.subjects[key]['ects']) + """</td>
                  </tr>
                  """)
    
def set_cookie():
    session_id=session.get_or_create_session_id()
    _, data=db.get_session(session_id)
    for key in form:
        status=form.getvalue(key)
        if status is not None:
            data[key]=status
    db.replace_session(session_id, data)

def print_cookie():
    session_id = session.get_or_create_session_id()
    _, data = db.get_session(session_id)
    zbroj_polozenih=0
    for key in podaci.subjects: 
        status=data.get(key, "Ne upisuje")
        if status=="Polozen":
            zbroj_polozenih = zbroj_polozenih + podaci.subjects[key]["ects"]
        subject_name=podaci.subjects[key]["name"]
        subject_ects=str(podaci.subjects[key]["ects"])
        print('<tr><td>'+subject_name+":" +'</td>'+ '<td>' + status +'</td>' + '<td>' + subject_ects + '</td>'+'</tr>')



set_cookie()
print()
base.start_html()
base.print_html()   
print_prvi_red()
printaj_imena(seleceted_year)
if(form.getvalue("key")=="Upisni list"):
    print_cookie()
base.end_html()

