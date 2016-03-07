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
    statement = '''select count(id) from temperature 
        where id ="%s" and datetime > DateAdd(MM, -1, GetDate())
        ;'''(id)
    c.execute(statement)
    user_stat['temperature'] = c.fetchall()

    statement = '''select count(id) from checks
        where id = "%s" and ref_type_id = 1 and 
        datetime > DateAdd(MM, -1, GetDate())
        ;'''(id)
    c.execute(statement)
    user_stat['Pest'] = c.fetchall()

    statement = '''select count(id) from checks
        where id = "%s" and ref_type_id=2 and 
        datetime > DateAdd(MM, -1, GetDate())
        ;'''(id)
    c.execute(statement)
    user_stat['Cleaning'] = c.fetchall()

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
