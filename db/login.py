import MySQLdb 

d= MySQLdb.connect(host = "kitchenkontrol.cpjb7blsswch.us-west-2.rds.amazonaws.com",
                 user = "Root",
                 passwd = "kitchenkontrol",
                 port = 3306,
                 db = "KitchenKontrol")


class Users():
    c = d.cursor()
    statement = "SHOW TABLES;"
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        print row

class check_password(passwd, username):
    c = d.cursor()
    statement = '''select count(id) from login
        where password = "%s and username =%s";''' (passwd, username)
    c.execute(statement)
    row = c.fetchall()
    def valid(self):
        if self.row ==1:
            return True
        else:
            return False

    
