import MySQLdb 

d = MySQLdb.connect(
    host="kitchenkontrol.cpjb7blsswch.us-west-2.rds.amazonaws.com",
    user="Root",
    passwd="kitchenkontrol",
    port=3306,
    db="KitchenKontrol")
