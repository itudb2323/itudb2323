import psycopg2

def get_db_data():
    conn = psycopg2.connect(database="Adventureworks", user="postgres", password="test", host="127.0.0.1", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT jobtitle, loginid FROM humanresources.employee")
    rows = cur.fetchall()
    return rows