from db import d


def get_user_id(email):
    c = d.cursor()
    statement = "SELECT Staff_Id FROM Staff join Login\
    ON Staff_id = Ref_Staff_id\
    WHERE email = '%s';" % (email)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        return row[0]


def get_email(u_id):
    c = d.cursor()
    statement = '''select email from Login
    WHERE ref_staff_id = %s;''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        return row[0]


def get_admin(u_id):
    c = d.cursor()
    statement = '''SELECT Admin FROM Login WHERE
    Ref_Staff_Id = %s;''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        return row[0]


def get_name(u_id):
    c = d.cursor()
    statement = '''SELECT First_Name from Staff
    where Staff_id = %s;''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        return row[0]


def get_user_contract(u_id):
    c = d.cursor()
    statement = '''SELECT contract from Staff
    where Staff_id = %s;''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        return row[0]
    


def get_notes(u_id):
    c = d.cursor()
    statement = '''SELECT notes FROM Notes n
    WHERE Ref_Staff_id = %s and DATE(n.date) =
    DATE(CURRENT_TIMESTAMP);''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        notes = row[0]
    if notes:
        return notes
    else:
        return "failed"


def set_notes(u_id, notes):
    c = d.cursor()
    statement = '''delete from Notes where
    Ref_Staff_id = %s;''' % (u_id)
    c.execute(statement)
    
    statement = '''INSERT INTO Notes VALUES (%s, CURRENT_TIMESTAMP,
    "%s");''' % (u_id, notes)
    c.execute(statement)
    d.commit()


def get_user_stat(u_id):
    user_stat = {}
    c = d.cursor()
    statement = '''select count(Ref_Staff_id) from Temperature 
        where Ref_Staff_id ="%s" and date(datetime) between 
        date(CURDATE())-INTERVAL 30 DAY AND CURDATE()
        ;''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        user_stat['Temperature'] = row[0]

    statement = '''select count(Ref_Staff_id) from Checks c
        where Ref_Staff_id = "%s" and ref_type_id = 1 and 
        date(c.date) between
        date(CURDATE())-INTERVAL 30 DAY AND CURDATE()
        ;''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        user_stat['Pest'] = row[0]

    statement = '''select count(Ref_Staff_id) from Checks c 
        where Ref_Staff_id = "%s" and ref_type_id=2 and 
        DATE(c.date) BETWEEN
        DATE(CURDATE())-INTERVAL 30 DAY AND CURDATE()
        ;''' % (u_id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        user_stat['Cleaning'] = row[0]

    return user_stat


def get_complete():
    complete = {}
    c = d.cursor()
    statement = '''SELECT COUNT(Batch_id) FROM Food_Processing
        where Activity = "Cooking";'''
    c.execute(statement)
    i = c.fetchall()
    if i == 1:
        complete['Cooking'] = True
    else:
        complete['Cooking'] = False

    statement = '''SELECT COUNT(Batch_id) FROM Food_Processing
        where Activity = "Cooling";'''
    c.execute(statement)
    i = c.fetchall()
    if i == 1:
        complete['Cooling'] = True
    else:
        complete['Cooling'] = False
    
    statement = '''SELECT COUNT(Batch_id) FROM Food_Processing
        where Activity = "Hot Hold";'''
    c.execute(statement)
    i = c.fetchall()
    if i == 1:
        complete['HotHold'] = True
    else:
        complete['HotHold'] = False
    
    return complete
