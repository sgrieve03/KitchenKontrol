import MySQLdb 
import string
import random
from werkzeug.security import generate_password_hash

d = MySQLdb.connect(host=
    "kitchenkontrol.cpjb7blsswch.us-west-2.rds.amazonaws.com",
    user="Root",
    passwd="kitchenkontrol",
    port=3306,
    db="KitchenKontrol")


class send():
    def validate(self, email):
        c = d.cursor()
        statement = '''select first_name 
            FROM Login join Staff on ref_staff_id = staff_id
            where email = "%s"'''\
            % (email)
        try:
            c.execute(statement)
            rows = c.fetchall()
            for row in rows:
                name = row[0]
                print name
            passwd = id_generator()
            print passwd

            password = generate_password_hash(passwd)
            statement = '''UPDATE Login SET password = "%s"
            where email = "%s";''' % (password, email)
            c.execute(statement)
            d.commit()
            return passwd
        except:
            return 'None'


def id_generator(size=7, chars=string.ascii_lowercase
        + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
