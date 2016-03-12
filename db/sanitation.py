from db import d


def create_strategy(ref_type, area, description, days):
    try:
        c = d.cursor()
        
        statement = '''INSERT INTO Strategy(ref_type_id, area, description)
        VALUES(%s, "%s", "%s");''' % (ref_type, area, description)
        c.execute(statement)
        d.commit()
        statement = '''SELECT strategy_id FROM Strategy
        WHERE area = "%s" and ref_type_id = %s;''' % (area, ref_type)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            areaid = row[0]
        print "areaid"
        print areaid
        print ref_type
        print days
        for day in days:
            statement = '''INSERT INTO Rota (ref_strategy_id,
            day) VALUES
            (%s, %s);''' % (areaid, day)
            c.execute(statement)
            d.commit()
            print "rota added"
        return True
    except: 
        return False


def get_todays_tasks(ref_type):
    try:    
        c = d.cursor()
        tasks = {}
        statement = '''SELECT strategy_id, Area FROM Strategy JOIN 
        Rota ON strategy_id = Ref_Strategy_Id 
        WHERE Day=DAYOFWEEK(CURRENT_TIMESTAMP) 
        and ref_type_id =%s;''' %(ref_type)

        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            tasks[row[0]] = {}
            tasks[row[0]]['area_id'] = row[0]
            tasks[row[0]]['area'] = row[1]

        return tasks
    except:
        return "None"


def get_overview(ref_type):
    try:
        c = d.cursor()
        overview = {}
        statement = '''SELECT s.strategy_id, s.area, s.description, c.ref_staff_id
        FROM Strategy s join Rota r ON s.strategy_id=r.ref_strategy_id
        LEFT JOIN Checks c on c.ref_strategy_id = s.strategy_id
        WHERE DAYOFWEEK(CURRENT_TIMESTAMP) = r.day and s.ref_type_id = %s;'''\
        % (ref_type)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            overview[row[0]] = {}
            overview[row[0]]["area_id"] = row[0]
            overview[row[0]]["area"] = row[1]
            overview[row[0]]["description"] = row[2]
            overview[row[0]]["staff_id"] = row[3]
        return overview
    except:
        return "None"
    

def create_check(ref_type, area, comment, ref_staff_id):
    print ref_type
    print area
    print comment
    print int(ref_staff_id)
    try:
        c = d.cursor()
        statement = '''SELECT Strategy_Id from Strategy WHERE
        Area = "%s" and ref_type_id= %s;''' % (area, ref_type)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            ref_area_id = int(row[0])
            print ref_area_id
        statement = '''INSERT INTO Checks(Ref_Type_id, ref_strategy_id,
        ref_staff_id, comment, complete) VALUES (%s, %s, %s, "%s", True);''' \
        % (ref_type, ref_area_id, int(ref_staff_id), comment)
        c.execute(statement)
        d.commit()
        return True
    except:
        return False 

