from db import d


def get_supplier():
    c = d.cursor()
    statement = "SELECT DISTINCT(Business_Name) FROM Suppliers;"
    c.execute(statement)
    rows = c.fetchall()
    suppliers = []
    for row in rows:
        suppliers.append(row)
    return suppliers
        

def get_items(business_name):
    c = d.cursor()
    statement = '''select item from approved_items
        where ref_supplier_id in (select supplier_id
        from Suppliers where business_name = "%s";'''(business_name)
    c.execute(statement)
    rows = c.fethall()
    items = []
    for row in rows:
        items.append(row)
    return items


def check_password(passwd, username):
    c = d.cursor()
    statement = '''select count(id) from login
        where password = "%s and username =%s";''' (passwd, username)
    c.execute(statement)
    row = c.fetchall()
    if row == 1:
            return True
    else:
            return False


def get_supplier_id(business_name):
    c = d.cursor()
    statement = '''SELECT Supplier_Id from Suppliers 
        WHERE business_name = "%s";'''(business_name)
    c.execute(statement)
    supplier_id = c.fetchall()
    return supplier_id


def add_item(business_name, invoice_number, used_by_date,
        item, temperature, thermometer, quantity, comment):
    supplier_id = get_supplier_id(business_name)
    c = d.cursor()
    
    statement = '''INSERT INTO Delivery(Invoice_Num, Ref_supplier_id)
    values ("%s", "%s);'''(invoice_number, supplier_id)
    c.execute(statement)
    statement = '''INSERT INTO Delivery_Item(
        ref_invoice_num, ref_approved_item_id, quantity, description,
        used_by_date, ref_appliance_id) values("%s", "%s", "s", "s",
        "%s", "%s";'''(invoice_number, approved_item_id, quantity,
        comment, used_by_date, appliance_id)









