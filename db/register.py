from werkzeug.security import generate_password_hash
from db import d


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
            Login where ref_staff_id = "%s";''' % (staff_id)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            num = int(row[0])
        if num == 0:
            passwd = generate_password_hash(passwd)
            statement = '''INSERT INTO Login VALUES
                ("%s","%s","%s");''' % (email, passwd, staff_id)
            c.execute(statement)
            d.commit()
            return True
        return False
    except:
        return False
