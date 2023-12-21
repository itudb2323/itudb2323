from flask import Blueprint, render_template, request
from model import get_employees, update_employee, add_employee 

index = Blueprint('index', __name__)

@index.route('/')
def home():
    data = get_employees()
    return render_template('index.html', items=data)

@index.route('/hire')
def hire():
    return render_template('hire.html')

@index.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        id = str(request.form.get('id'))
        print(id.__class__)
        item = update_employee(id)
        return render_template('update.html', item=item)
    else:
        item = update_employee(id)
        return render_template('update.html', item=item)