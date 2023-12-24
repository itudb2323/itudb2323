import psycopg2

def get_employees():
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT employee.jobtitle, person.firstname, person.middlename, person.lastname, employee.businessentityid FROM humanresources.employee join person.person on employee.businessentityid = person.businessentityid")
    rows = cur.fetchall()
    return rows

def get_employee(id):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"SELECT employee.jobtitle, person.firstname, person.middlename, person.lastname, person.businessentityid FROM humanresources.employee join person.person on employee.businessentityid = person.businessentityid where employee.businessentityid = {id}",)
    row = cur.fetchall()
    return row

def update_employee(id, firstname, middlename, lastname, jobtitle):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"UPDATE person.person SET firstname = \'{firstname}\', middlename = \'{middlename}\', lastname = \'{lastname}\' WHERE businessentityid = {id}")
    conn.commit()
    cur.execute(f"UPDATE humanresources.employee SET jobtitle = \'{jobtitle}\' WHERE businessentityid = {id}")
    conn.commit()

def add_employee():
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("")

def delete_employee(id):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM humanresources.employee WHERE businessentityid = {id}")
    conn.commit()
