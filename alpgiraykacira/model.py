import psycopg2

connection_string = "dbname='Adventureworks' user='postgres' password='postgres' host='localhost' port='5432'"


def getOrders(orderby='soh.salesorderid'):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT soh.salesorderid, soh.orderdate, soh.duedate, soh.shipdate, soh.status,"
        f"sod.carriertrackingnumber, sod.orderqty, sod.unitprice, (sod.orderqty * sod.unitprice) totalprice, "
        f"p.name, p.productnumber, p.color, c.customerid, s.name, sod.salesorderdetailid "
        f"FROM sales.salesorderheader soh "
        f"LEFT JOIN sales.salesorderdetail sod ON sod.salesorderid = soh.salesorderid "
        f"LEFT JOIN production.product p ON p.productid = sod.productid "
        f"LEFT JOIN sales.customer c ON c.customerid = soh.customerid "
        f"LEFT JOIN sales.store s ON s.businessentityid = c.storeid "
        f"ORDER BY {orderby} "
        f"LIMIT 500"
    )
    rows = cur.fetchall()
    return rows


def getOrderDetails(order_id):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT sod.salesorderdetailid, sod.carriertrackingnumber, sod.orderqty, sod.unitprice, "
        f"(sod.orderqty * sod.unitprice) totalprice, "
        f"p.name, p.productnumber, p.color "
        f"FROM sales.salesorderdetail sod "
        f"LEFT JOIN production.product p ON p.productid = sod.productid "
        f"WHERE sod.salesorderid = {order_id}"
    )
    rows = cur.fetchall()
    return rows


def updateOrderDetails(order_detail_id, order_qty, unit_price):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"UPDATE sales.salesorderdetail "
        f"SET orderqty = {order_qty}, unitprice = {unit_price} "
        f"WHERE salesorderdetailid = {order_detail_id}"
    )
    conn.commit()


def deleteOrderDetail(order_detail_id):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"DELETE FROM sales.salesorderdetail "
        f"WHERE salesorderdetailid = {order_detail_id}"
    )
    cur.execute(
        f"DELETE FROM sales.salesorderheader "
        f"WHERE salesorderid NOT IN (SELECT salesorderid FROM sales.salesorderdetail)"
    )
    conn.commit()


def addOrder(customer_id, order_date, due_date, ship_date, status, carrier_tracking_number, order_qty, unit_price,
             product_id, sales_person_id, territory_id, bill_to_address_id, ship_to_address_id, ship_method_id,
             credit_card_id, currency_rate_id, special_offer_id):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO sales.salesorderheader (customerid, orderdate, duedate, shipdate, status, "
        f"salespersonid, territoryid, billtoaddressid, shiptoaddressid, shipmethodid, creditcardid, "
        f"creditcardapprovalcode, currencyrateid, subtotal, taxamt, freight, totaldue, comment, modifieddate) "
        f"VALUES ({customer_id}, '{order_date}', '{due_date}', '{ship_date}', {status}, "
        f"{sales_person_id}, {territory_id}, {bill_to_address_id}, {ship_to_address_id}, {ship_method_id}, "
        f"{credit_card_id}, '123', {currency_rate_id}, 0, 0, 0, 0, 'Test', '2023-12-24') "
        f"RETURNING salesorderid"
    )
    order_id = cur.fetchone()[0]
    cur.execute(
        f"SELECT 1 FROM sales.specialofferproduct "
        f"WHERE specialofferid = {special_offer_id} AND productid = {product_id}"
    )
    pair_exists = cur.fetchone()

    if not pair_exists:
        cur.execute(
            f"INSERT INTO sales.specialofferproduct (specialofferid, productid) "
            f"VALUES ({special_offer_id}, {product_id})"
        )

    cur.execute(
        f"INSERT INTO sales.salesorderdetail (salesorderid, productid, carriertrackingnumber, specialofferid, "
        f"orderqty, unitprice) "
        f"VALUES ({order_id}, {product_id}, '{carrier_tracking_number}', '{special_offer_id}', {order_qty}, "
        f"{unit_price})"
    )
    conn.commit()


def getCustomers():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT customerid FROM sales.customer"
    )
    rows = cur.fetchall()
    return rows


def getSalesPerson():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT businessentityid FROM sales.salesperson"
    )
    rows = cur.fetchall()
    return rows


def getSalesTerritory():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT territoryid FROM sales.salesterritory"
    )
    rows = cur.fetchall()
    return rows


def getBillToAddress():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT addressid FROM person.address"
    )
    rows = cur.fetchall()
    return rows


def getShipToAddress():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT addressid FROM person.address"
    )
    rows = cur.fetchall()
    return rows


def getShipMethod():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT shipmethodid FROM purchasing.shipmethod"
    )
    rows = cur.fetchall()
    return rows


def getCreditCard():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT creditcardid FROM sales.creditcard"
    )
    rows = cur.fetchall()
    return rows


def getCurrencyRate():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT currencyrateid FROM sales.currencyrate"
    )
    rows = cur.fetchall()
    return rows


def getSpecialOffer():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT specialofferid FROM sales.specialoffer"
    )
    rows = cur.fetchall()
    return rows


def getProducts():
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute(
        f"SELECT productid FROM production.product"
    )
    rows = cur.fetchall()
    return rows
