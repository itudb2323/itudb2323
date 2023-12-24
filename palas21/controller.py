from flask import Blueprint, render_template, request, redirect, url_for
from model import get_employees,get_employee, update_employee, add_employee , delete_employee, search_employee_name, search_employee_job, get_employee_info

index = Blueprint('index', __name__)

@index.route('/')
def home():
    data = get_employees()
    return render_template('main.html', items=data)

@index.route('/hire')
def hire():
    return render_template('hire.html')

@index.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        item = get_employee(id)
        return render_template('update.html', item=item)
    else:
        item = get_employee(id)
        return render_template('update.html', item=item)

@index.route('/update/<id>/<firstname>/<middlename>/<lastname>/<jobtitle>', methods=['GET','POST'])
def update_completed(id,firstname,middlename,lastname,jobtitle):
    jobtitle = jobtitle.replace("_", " ")
    if request.method == 'GET':
        update_employee(id, firstname, middlename, lastname, jobtitle)
        return redirect(url_for('index.home'))
    else:
        return redirect(url_for('index.home'))
    
@index.route('/fire/<id>', methods=['GET', 'POST'])
def fire(id):
    if request.method == 'GET':
        delete_employee(id)
        return redirect(url_for('index.home'))
    else:
        return redirect(url_for('index.home'))
    
@index.route('/hire/<firstname>/<middlename>/<lastname>/<jobtitle>', methods=['GET','POST'])
def hire_completed(firstname,middlename,lastname,jobtitle):
    jobtitle = jobtitle.replace("_", " ")
    if request.method == 'GET':
        add_employee(firstname, middlename, lastname, jobtitle)
        return redirect(url_for('index.home'))
    else:
        return redirect(url_for('index.home'))
    
@index.route('/action_page')
def search():
    search_type = request.args.get('search_type')
    search = request.args.get('search')
    if search == '':
        return redirect(url_for('index.home'))
    if search_type == 'fullname':
        data = search_employee_name(search)
    elif search_type == 'jobtitle':
        data = search_employee_job(search)
    else:
        data = []
    return render_template('main.html', items=data)

@index.route('/employee_info/<id>')
def employee_info(id):
    item = get_employee_info(id)
    return render_template('employee_info.html', items=item)