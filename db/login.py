import MySQLdb 
from werkzeug.security import check_password_hash

d = MySQLdb.connect (host=
    "kitchenkontrol.cpjb7blsswch.us-west-2.rds.amazonaws.com",
    user="Root",
    passwd="kitchenkontrol",
    port=3306,
    db="KitchenKontrol")


class check_password ():
    def validate (self, passwd, email):

        c = d.cursor()
        statement = '''select password from Login
            where email ="%s";'''\
            %(email)
        try:
            c.execute(statement)
            rows = c.fetchall()
            for row in rows:
                password = row[0]
            print password
            print passwd
            print email
            if check_password_hash(password,passwd):     
                return True
        except:
            return False

    
