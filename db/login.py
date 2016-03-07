from werkzeug.security import check_password_hash
from db import d


class check_password ():
    def validate(self, passwd, email):

        c = d.cursor()
        statement = '''select password from Login
            where email ="%s";'''\
            % (email)
        try:
            c.execute(statement)
            rows = c.fetchall()
            for row in rows:
                password = row[0]
            if check_password_hash(password, passwd):     
                return True
        except:
            return False

    
