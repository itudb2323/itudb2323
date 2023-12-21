import psycopg2

def get_employees():
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT employee.jobtitle, person.firstname, person.middlename, person.lastname, employee.businessentityid FROM humanresources.employee join person.person on employee.businessentityid = person.businessentityid")
    rows = cur.fetchall()
    return rows

def update_employee(id):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT employee.jobtitle, person.firstname, person.middlename, person.lastname FROM humanresources.employee join person.person on employee.businessentityid = person.businessentityid where employee.businessentityid = %s", (id,))
    row = cur.fetchall()
    return row

def add_employee():
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("")