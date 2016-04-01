from db import d


def get_suppliers():
    try:
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
    except:
        pass


def get_thermometers():
    try:
        c = d.cursor()
        statement = '''SELECT thermometer_id, cooked_stat FROM Thermometer
        WHERE current = true;'''
        c.execute(statement)
        rows = c.fetchall()
        thermometers = {}
        for row in rows:
            thermometers[row[0]] = {}
            thermometers[row[0]]['id'] = row[0]
            thermometers[row[0]]['stat'] = row[1]
        return thermometers
    except:
        pass


def get_appliances():
    try:
        c = d.cursor()
        statement = '''SELECT Appliance_Id FROM Appliance
        WHERE current = true;'''
        c.execute(statement)
        rows = c.fetchall()
        appliances = []
        for row in rows:
            appliances.append(row[0])
        return appliances
    except:
        pass


def checkInvoice(num):
    try:
        c = d.cursor()
        statement = '''SELECT COUNT(Invoice_Num) FROM Delivery
            WHERE Invoice_Num = "%s";''' % (num)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            num = row[0]
        if num > 0:
            return True
        else:
            return False
    except:
        pass


def get_items(business_name):
    try:
        c = d.cursor()
        statement = '''select item from Approved_Items 
        where current = True and ref_supplier_id = (select supplier_id
        from Suppliers where current = True and 
        business_name = "%s");''' % (business_name)
        c.execute(statement)
        rows = c.fetchall()
        items = {}
        for row in rows:
            items[row[0]] = row[0]
        return items
    except:
        pass


def get_edit_items(Invoice_Num):
    try:
        c = d.cursor()
        statement = '''select item from Approved_Items 
        where approved_item_id in 
        (select ref_approved_item_id from 
        Delivery_Item where ref_invoice_num = "%s")
        ;''' % (Invoice_Num)
        c.execute(statement)
        rows = c.fetchall()
        items = {}
        for row in rows:
            items[row[0]] = row[0]
        return items
    except:
        pass


def loaditem(item, invoice):
    try:
        load = {}
        c = d.cursor()
        indic = invoice + ": " + item
        statement = '''SELECT temperature, ref_thermometer_id
        FROM Temperature WHERE Item_Indicator =
        "%s";''' % (indic)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            load['temperature'] = row[0]
            load['thermometer'] = row[1]
        statement = ''' SELECT quantity, description, used_by_date,
        ref_appliance_id FROM Delivery_Item JOIN Approved_Items
        on ref_supplier_id = ref_supplier_id WHERE ref_invoice_num
        = "%s" and item = "%s";''' % (invoice, item)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            load['qty'] = row[0]
            load['status'] = row[1]
            load['used_by'] = row[2]
            load['destination'] = row[3]
        return load
    except:
        pass


def get_supplier_id(business_name):
    try:
        c = d.cursor()
        statement = '''SELECT Supplier_Id from Suppliers 
            WHERE current =true and business_name = "%s";''' % (business_name)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            supplier_id = row[0]
        return supplier_id
    except:
        pass


def get_order_invoice(business_name):
    try:
        supplier_id = get_supplier_id(business_name)
        c = d.cursor()
        statement = '''SELECT invoice_num FROM Delivery WHERE
        ref_Supplier_id = "%s" AND 
        DATE(DATETIME) = DATE(CURRENT_TIMESTAMP);''' % (supplier_id)
        c.execute(statement)
        rows = c.fetchall()
        for row in rows:
            invoice_number = row[0]
        return invoice_number 
    except:
        pass


def get_approved_item_id(item, supplier_id):
        c = d.cursor()
        statement = '''Select approved_item_id from Approved_Items
        where current = true and
        item = "%s" and ref_supplier_id = "%s";''' % (item, supplier_id)
        c.execute(statement)
        items = c.fetchall()
        print items
        for i in items:
            print i[0]
            item_id = i[0]
        return item_id


def start_new_delivery(business_name, invoice_number):
    try:
        supplier_id = get_supplier_id(business_name)
        c = d.cursor()
        statement = '''INSERT INTO Delivery(Invoice_Num, Ref_supplier_id)
        values ("%s", "%s");''' % (invoice_number, supplier_id)
        c.execute(statement)
        d.commit()
    except:
        pass


def add_delivered_item(business_name, invoice_number, used_by_date,
        item, temperature, appliance_id, thermometer,
        quantity, comment, staff_id):
        supplier_id = get_supplier_id(business_name)
        print supplier_id
        print item
        c = d.cursor()
        item_id = get_approved_item_id(item, supplier_id)
        print item_id
        statement = '''INSERT INTO Delivery_Item(
            ref_invoice_num, ref_approved_item_id, quantity, description,
            used_by_date, ref_appliance_id) values("%s", "%s", %s, "%s",
            "%s", %s);''' % (invoice_number, item_id, quantity,
            comment, used_by_date, appliance_id)
        c.execute(statement)
        d.commit()
        item_indicator = invoice_number + ": " + item
        statement = '''INSERT INTO Temperature(item_indicator,
        ref_staff_id,ref_thermometer_id, temperature)VALUES
        ("%s", %s, %s, %s);''' % (item_indicator, staff_id,
            thermometer, temperature)
        c.execute(statement)
        d.commit()


def update_delivered_item(business_name, invoice_number, used_by_date,
        item, temperature, appliance_id, thermometer,
        quantity, comment, staff_id):
    try:
        supplier_id = get_supplier_id(business_name)
        c = d.cursor()
        item_id = get_approved_item_id(item, supplier_id)
        statement = '''UPDATE Delivery_Item SET
            quantity = %s, description = "%s", used_by_date = "%s",
            ref_appliance_id = %s WHERE ref_invoice_num ="%s"
            AND ref_approved_item_id ="%s";''' % (quantity,
            comment, used_by_date, appliance_id, invoice_number, item_id)
        c.execute(statement)
        d.commit()
        item_indicator = invoice_number + ": " + item
        statement = '''UPDATE Temperature SET ref_staff_id =%s,
        ref_thermometer_id = %s, temperature = %s
        WHERE Item_Indicator = "%s";''' % (staff_id,
            thermometer, temperature, item_indicator)
        c.execute(statement)
        d.commit()
        return True
    except:
        pass


def delete_Approved_item(item, supplier_id):
    try:
        c = d.cursor()
        statement = '''UPDATE Approved_Items SET current = False
            WHERE item = "%s" and supplier_id = "%s";''' % (item,
                supplier_id)
        c.execute(statement)
        d.commit()
        return True
    except:
        pass

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


def add_supplier(bname, stele, atele, first_line, second_line, third_line,
        town, postcode):
    try:
        import random
        print "length:"
        print len(postcode)
        supplier_id = (bname.upper()[:2] +
            str(random.randrange(1000, 2000, 1)))
        a = d.cursor()
        statement = '''INSERT INTO Suppliers (Supplier_id, Business_name)
            VALUES ("%s", "%s");''' % (supplier_id, bname)
        a.execute(statement)
        b = d.cursor()
        statement = '''INSERT INTO Telephone VALUES ("%s", "%s", "%s")
            ;''' % (supplier_id, stele, "sales")
        b.execute(statement)
        c = d.cursor()
        statement = '''INSERT INTO Telephone VALUES ("%s", "%s", "%s")
            ;''' % (supplier_id, atele, "accounts")
        c.execute(statement)
        e = d.cursor()
        statement = '''INSERT INTO Address VALUES ("%s", "%s", "%s", "%s", "%s",
        "%s") ;''' % (supplier_id, first_line, second_line, third_line, town,
            postcode)
        e.execute(statement)
        d.commit()
        return True
    except:
        return False
