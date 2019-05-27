from sqlalchemy.exc import IntegrityError, InvalidRequestError


def get_customer(data_row):
    customer_data = {
        'id': int(data_row[0]),
        'first_name': data_row[1],
        'last_name': data_row[2],
        'street_address': data_row[3],
        'state': data_row[4].upper(),
        'zipcode': data_row[5],
    }

    return customer_data


def get_product(data_row):
    product_data = {
        'id': int(data_row[7]),
        'name': data_row[8]
    }
    return product_data


def get_order_status(data_row):
    order_data = {
        'price': data_row[9],
        'status': data_row[6].lower(),
        'created_at': data_row[10],
        'updated_at': data_row[10]
    }
    return order_data


def insert_row(session, data, logger):
    try:
        session.add(data)
        session.flush()
    except IntegrityError or InvalidRequestError:
        session.rollback()
        related_ids = data.id or {'customer': data.customer_id, 'product': data.product_id}
        logger.warn('Record already exists: {} {}'.format(data.__class__.__name__, related_ids))


def process_order(order):
    customer = get_customer(order)
    product = get_product(order)
    order_status = get_order_status(order)
    previous_order = None

    if order_status['status'] == 'canceled':
        previous_order = {'customer_id': customer['id'],
                          'product_id': product['id']}
    else:
        order_status['customer_id'] = customer['id']
        order_status['product_id'] = product['id']

    return customer, product, order_status, previous_order
