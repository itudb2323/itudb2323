from flask import Blueprint, render_template, request, redirect, url_for
from model import get_employees,get_employee, update_employee, add_employee , delete_employee

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