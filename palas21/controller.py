from flask import Blueprint, render_template
from model import get_db_data

index = Blueprint('index', __name__)

@index.route('/')
def home():
    data = get_db_data()
    return render_template('index.html', items=data)