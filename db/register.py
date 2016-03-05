import MySQLdb 
from werkzeug.security import generate_password_hash

d = MySQLdb.connect (host=
    "kitchenkontrol.cpjb7blsswch.us-west-2.rds.amazonaws.com",
    user="Root",
    passwd="kitchenkontrol",
    port=3306,
    db="KitchenKontrol")


def validate(firstname, lastname, email, passwd):
    c = d.cursor()
    statement = '''select staff_id from Staff
        where first_name ="%s" and last_name ="%s";'''\
        % (firstname, lastname)
    try:
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            staff_id = int(row[0])
        print staff_id
        statement = '''select count(ref_staff_id) from
            Login where ref_staff_id = "%s";'''%(staff_id)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            num = int(row[0])
        if num == 0:
            passwd = generate_password_hash(passwd)
            statement = '''INSERT INTO Login VALUES
                ("%s","%s","%s");'''%(email, passwd, staff_id)
            c.execute(statement)
            d.commit()
            d.close()
            return True
        return False
    except:
        d.close()
        return False


    
