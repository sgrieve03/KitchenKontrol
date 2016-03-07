from db import d


def create_cleaning_strategy(area, description, days):
    try:
        c = d.cursor()
        
        statement = '''INSERT INTO Cleaning_Strategy(area, description)
        VALUES("%s", "%s");'''(area, description)
        c.execute(statement)
        
        statement = '''SELECT Area_id FROM Cleaning_Strategy
        WHERE area = "%s";'''(area)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            id = row[0]

        for day in days:
            statement = '''INSERT INTO Cleaning_Rota VALUES
            ("%s", "%s");''' % (id, day)
            c.execute(statement)

        d.commit()
        return True
    except: 
        return False


def get_todays_cleaning_tasks():
    try:    
        c = d.cursor()
        tasks = {}
        statement = '''SELECT Area_id, Area FROM Cleaning_Strategy JOIN 
        Cleaning_Rota ON Area_id = Ref_Area_Id 
        WHERE Day=DAYOFWEEK(CURRENT_TIMESTAMP);'''

        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            tasks[row[0]] = {}
            tasks[row[0]]['area_id'] = row[0]
            tasks[row[0]]['area'] = row[1]

        return tasks
    except:
        return "None"


def get_cleaning_overview():
    try:
        c = d.cursor()
        overview = {}
        statement = '''SELECT s.area_id, s.area, s.description, c.ref_staff_id
        FROM Cleaning_Strategy s join Cleaning_Rota r ON s.area_id=r.ref_area_id
        LEFT JOIN Checks c on c.ref_area_id = s.area_id
        WHERE DAYOFWEEK(CURRENT_TIMESTAMP) = r.day;'''
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
    

def create_check(ref_area_id, comment, ref_staff_id):
    try:
        c = d.cursor()
        statement = '''INSERT INTO Checks(ref_type_id, ref_area_id, comment,
        ref_staff_id) VALUES (2, "%s", "%s", "%s";''' \
        % (ref_area_id, comment, ref_staff_id)
        c.execute(statement)
        d.commit()
        return True
    except:
        return False 

