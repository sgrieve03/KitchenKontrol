from db import d


def get_suppliers():
    c = d.cursor()
    statement = '''SELECT DISTINCT(Business_Name) 
    FROM Suppliers
    WHERE current = true;'''
    c.execute(statement)
    rows = c.fetchall()
    suppliers = []
    for row in rows:
        suppliers.append(row)
    return suppliers
       

def get_thermometers():
    c = d.cursor()
    statement = '''SELECT thermometer_id FROM Thermometer
    WHERE current = true;'''
    c.execute(statement)
    rows = c.fetchall()
    thermometers = []
    for row in rows:
        thermometers.append(row[0])
    return thermometers


def get_appliances():
    c = d.cursor()
    statement = '''SELECT Appliance_Id FROM Appliance
    WHERE current = true;'''
    c.execute(statement)
    rows = c.fetchall()
    appliances = []
    for row in rows:
        appliances.append(row[0])
    return appliances


def get_items(business_name):
    print business_name
    c = d.cursor()
    statement = '''select item from Approved_Items 
    where current = True and ref_supplier_id = (select supplier_id
    from Suppliers where current = True and 
    business_name = "%s");''' % (business_name)
    print statement
    c.execute(statement)
    rows = c.fetchall()
    items = {}
    for row in rows:
        items[row[0]] = row[0]
    return items


def get_supplier_id(business_name):
    c = d.cursor()
    statement = '''SELECT Supplier_Id from Suppliers 
        WHERE current =true and business_name = "%s";''' % (business_name)
    c.execute(statement)
    rows = c.fetchall()
    for row in rows:
        supplier_id = row[0]
        print supplier_id
    return supplier_id


def get_approved_item_id(item, supplier_id):
    c = d.cursor()
    statement = '''Select approved_item_id from Approved_Items
    where current = true and
    item = "%s" and ref_supplier_id = "%s";''' % (item, supplier_id)
    c.execute(statement)
    items = c.fetchall()
    for item in items:
        item_id = item[0]
    return item_id


def start_new_delivery(business_name, invoice_number):
    supplier_id = get_supplier_id(business_name)
    c = d.cursor()
    statement = '''INSERT INTO Delivery(Invoice_Num, Ref_supplier_id)
    values ("%s", "%s");''' % (invoice_number, supplier_id)
    c.execute(statement)
    d.commit()
    print "add to delivery stage 1"


def add_delivered_item(business_name, invoice_number, used_by_date,
        item, temperature, appliance_id, thermometer,
        quantity, comment, staff_id):
    supplier_id = get_supplier_id(business_name)
    c = d.cursor()
    item_id = get_approved_item_id(item, supplier_id)
    print supplier_id
    print item_id
    print used_by_date
    print invoice_number
    print business_name
    print temperature
    print thermometer
    statement = '''INSERT INTO Delivery_Item(
        ref_invoice_num, ref_approved_item_id, quantity, description,
        used_by_date, ref_appliance_id) values("%s", "%s", %s, "%s",
        "%s", %s);''' % (invoice_number, item_id, quantity,
        comment, used_by_date, appliance_id)
    c.execute(statement)
    d.commit()
    print "add to delivery stage2"
    item_indicator = invoice_number + ": " + item
    print item_indicator
    statement = '''INSERT INTO Temperature(item_indicator,
    ref_staff_id,ref_thermometer_id, temperature)VALUES
    ("%s", %s, %s, %s);''' % (item_indicator, staff_id,
        thermometer, temperature)
    c.execute(statement)
    d.commit()
    print "add to delivery complete"
    return True


def delete_Approved_item(item, supplier_id):
    c = d.cursor()
    statement = '''UPDATE Approved_Items SET current = False
        WHERE item = "%s" and supplier_id = "%s";''' % (item,
            supplier_id)
    c.execute(statement)
    d.commit()
    return True


def get_deleted_approved_items(supplier_id):
    c = d.cursor()
    statement = '''SELECT Approved_item_id, Item, Cooked_Stat,
    temp_stat FROM Approved_items WHERE Current = False;'''
    c.execute(statement)
    rows = c.fetchall()
    deleted_items = {}
    for row in rows:
        deleted_items[row[0]] = {}
        deleted_items[row[0]]['Approved_item_id'] = row[0]
        deleted_items[row[0]]['Item'] = row[1]
        deleted_items[row[0]]['Cooked_Stat'] = row[2]
        deleted_items[row[0]]['Temp_Stat'] = row[3]
    return deleted_items


def get_todays_suppliers():
    c = d.cursor()
    statement = '''SELECT Business_Name from Suppliers JOIN
    Delivery ON  Supplier_id = Ref_Supplier_id WHERE Supplier_id 
    IN (SELECT Ref_Supplier_id FROM Delivery WHERE DATE(Datetime)
    = DATE(CURRENT_TIMESTAMP));'''
    c.execute(statement)
    rows = c.fetchall()
    suppliers = {}
    for row in rows:
        suppliers[row[0]] = row[0]
    print "got todays suppliers"
    print suppliers
    return suppliers

def get_overview():
    c = d.cursor()
    statement = '''SELECT di.delivery_item_id, ai.ref_supplier_id, 
    d.invoice_num, ai.item, di.quantity, di.used_by_date 
    FROM Delivery_Item di JOIN Approved_Items ai on
    ai.Approved_Item_id = di.Ref_Approved_Item_id join 
    Delivery d on d.invoice_num = di.ref_invoice_num 
    WHERE di.cancelled = False
    AND date(d.datetime)=date(CURRENT_TIMESTAMP);'''
    c.execute(statement)
    rows = c.fetchall()
    overview = {}
    for row in rows:
        overview[row[0]] = {}
        overview[row[0]]['delivery_item_id'] = row[0]
        overview[row[0]]['supplier_id'] = row[1]
        overview[row[0]]['invoice_num'] = row[2]
        overview[row[0]]['item'] = row[3]
        overview[row[0]]['qty'] = row[4]
        overview[row[0]]['used_by_date'] = row[5]
    return overview
