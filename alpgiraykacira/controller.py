from flask import Blueprint, render_template, request, redirect, url_for
from model import getOrders, updateOrderDetails, deleteOrderDetail, getCustomers, addOrder, getSalesPerson, \
    getSalesTerritory, getBillToAddress, getShipToAddress, getShipMethod, getCreditCard, getCurrencyRate, \
    getSpecialOffer, getProducts

index = Blueprint('index', __name__)


@index.route('/', methods=['GET', 'POST'])
def home():
    orderby = request.args.get('orderby', 'soh.salesorderid')
    data = getOrders(orderby)

    bikeshop_filter = request.args.get('bikeshop', 'all')

    if request.method == 'POST':
        order_detail_id = request.form.get('order_detail_id')

        if 'update' in request.form:
            order_qty = request.form.get('order_qty')
            unit_price = request.form.get('unit_price')
            updateOrderDetails(order_detail_id, order_qty, unit_price)
        elif 'delete' in request.form:
            deleteOrderDetail(order_detail_id)

        return redirect(url_for('index.home'))

    filtered_data = data
    if bikeshop_filter != 'all':
        filtered_data = [item for item in data if item[13] == bikeshop_filter]

    bikeshops = set(item[13] for item in data)
    return render_template('index.html', items=filtered_data, bikeshops=bikeshops,
                           selected_bikeshop=bikeshop_filter, selected_orderby=orderby)


@index.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        order_date = request.form.get('order_date')
        due_date = request.form.get('due_date')
        ship_date = request.form.get('ship_date')
        status = request.form.get('status')
        carrier_tracking_number = request.form.get('carrier_tracking_number')
        order_qty = request.form.get('order_qty')
        unit_price = request.form.get('unit_price')
        product_id = request.form.get('product_id')
        sales_person_id = request.form.get('sales_person_id')
        territory_id = request.form.get('sales_territories')
        bill_to_address_id = request.form.get('bill_to_address_id')
        ship_to_address_id = request.form.get('ship_to_address_id')
        ship_method_id = request.form.get('ship_method_id')
        credit_card_id = request.form.get('credit_card_id')
        currency_rate_id = request.form.get('currency_rate_id')
        special_offer_id = request.form.get('special_offer_id')

        addOrder(customer_id, order_date, due_date, ship_date, status, carrier_tracking_number, order_qty, unit_price,
                 product_id, sales_person_id, territory_id, bill_to_address_id, ship_to_address_id, ship_method_id,
                 credit_card_id, currency_rate_id, special_offer_id)

        return redirect(url_for('index.home'))

    customers = getCustomers()
    products = getProducts()
    sales_persons = getSalesPerson()
    sales_territories = getSalesTerritory()
    bill_to_addresses = getBillToAddress()
    ship_to_addresses = getShipToAddress()
    ship_methods = getShipMethod()
    credit_cards = getCreditCard()
    currency_rates = getCurrencyRate()
    special_offers = getSpecialOffer()

    return render_template('add_order.html', customers=customers, sales_persons=sales_persons,
                           sales_territories=sales_territories, bill_to_addresses=bill_to_addresses,
                           ship_to_addresses=ship_to_addresses, ship_methods=ship_methods, credit_cards=credit_cards,
                           currency_rates=currency_rates, special_offers=special_offers, products=products)
