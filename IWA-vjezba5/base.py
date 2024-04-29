#!python.exe


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
          
     """)

def print_html():
    print("""
          <form method="POST">
          <th>
          <input type="submit" name="key" value="1st Year">
          <input type="submit" name="key" value="2nd Year">
          <input type="submit" name="key" value="3rd Year">
          <input type="submit" name="key" value="Upisni list">  
          <input type="submit" name="key" value="Logout">
          <input type="submit" name="key" value="Change Password">
          </th>
          <table>
          """)

def end_html():
    print("""
          </table>
          </form>
          </body>
    </html>
    """)

