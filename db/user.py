from db import d


def get_user(email):
    c = d.cursor()
    statement = "SELECT Staff_Id FROM Staff join Login\
    ON Staff_id = Ref_Staff_id\
    WHERE email = '%s';" % (email)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        return row[0]


def get_user_stat(id):
    user_stat = {}
    c = d.cursor()
    statement = '''select count(Ref_Staff_id) from Temperature 
        where Ref_Staff_id ="%s" and date(datetime) between 
        date(CURDATE())-INTERVAL 30 DAY AND CURDATE()
        ;''' % (id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        user_stat['Temperature'] = row[0]

    statement = '''select count(Ref_Staff_id) from Checks c
        where Ref_Staff_id = "%s" and ref_type_id = 1 and 
        date(c.date) between
        date(CURDATE())-INTERVAL 30 DAY AND CURDATE()
        ;''' % (id)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        user_stat['Pest'] = row[0]

    statement = '''select count(Ref_Staff_id) from Checks c 
        where Ref_Staff_id = "%s" and ref_type_id=2 and 
        DATE(c.date) BETWEEN
        DATE(CURDATE())-INTERVAL 30 DAY AND CURDATE()
        ;''' % (id)
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
