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

def add_employee(firstname, middlename,lastname,jobtitle):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"insert into person.person (firstname, middlename,lastname) values (\'{firstname}\',\'{middlename}\',\'{lastname}\')")
    conn.commit()
    cur.execute(f"insert into humanresources.employee (businessentityid,jobtitle) values (\'{jobtitle}\')")
    conn.commit()

def delete_employee(id):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM humanresources.employee WHERE businessentityid = {id}")
    conn.commit()

def search_employee_name(fullname):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"SELECT employee.jobtitle, person.firstname, person.middlename, person.lastname, person.businessentityid FROM humanresources.employee join person.person on employee.businessentityid = person.businessentityid where lower(person.firstname) like lower(\'%{fullname}%\') or lower(person.middlename) like lower(\'%{fullname}%\') or lower(person.lastname) like lower(\'%{fullname}%\')")
    rows = cur.fetchall()
    return rows

def search_employee_job(jobtitle):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"SELECT employee.jobtitle, person.firstname, person.middlename, person.lastname, person.businessentityid FROM humanresources.employee join person.person on employee.businessentityid = person.businessentityid where lower(employee.jobtitle) like lower(\'%{jobtitle}%\')")
    rows = cur.fetchall()
    return rows

def get_employee_info(id):
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute(f"""SELECT
    P.BusinessEntityID,
    P.PersonType,
    P.NameStyle,
    P.Title,
    P.FirstName,
    P.MiddleName,
    P.LastName,
    P.Suffix,
    P.EmailPromotion,
    P.AdditionalContactInfo,
    P.Demographics,
    P.rowguid AS PersonRowGuid,
    P.ModifiedDate AS PersonModifiedDate,
    E.NationalIDNumber,
    E.LoginID,
    E.JobTitle,
    E.BirthDate,
    E.MaritalStatus,
    E.Gender,
    E.HireDate,
    E.SalariedFlag,
    E.VacationHours,
    E.SickLeaveHours,
    E.CurrentFlag,
    E.rowguid AS EmployeeRowGuid,
    E.ModifiedDate AS EmployeeModifiedDate
FROM
   person.Person AS P
JOIN
    humanresources.Employee AS E ON P.BusinessEntityID = E.BusinessEntityID
WHERE P.BusinessEntityID = {id}
""")
    row = cur.fetchall()
    return row