import os
import csv
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

from utils import process_order, insert_row

# CONFIG
app = Flask(__name__)
app.config.from_pyfile('application.cfg')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# MODELS
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    street_address = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class OrderStatus(db.Model):
    __tablename__ = 'order_statuses'
    __table_args__ = (db.UniqueConstraint('customer_id', 'product_id', name='customer_product_uc'),)

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum("new", "canceled", name="order_enum", create_type=False))
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)


# VIEWS
@app.route('/')
def upload():
    return render_template("upload.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file_obj = request.files['file']

        if file_obj.filename == '' or file_obj.filename.split('.')[-1] != 'tsv':
            error = 'Invalid file!'
            return render_template('upload.html', error=error)

        if file_obj:
            filename = secure_filename(file_obj.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_obj.save(file_path)

        with open(file_path) as order_data:
            reader = csv.reader(order_data, delimiter='\t')

            app.logger.info('Begin processing File')

            for row in reader:
                customer, product, order_status, previous_order = process_order(row)

                if not previous_order:
                    insert_row(db.session, Customer(**customer), app.logger)
                    insert_row(db.session, Product(**product), app.logger)
                    insert_row(db.session, OrderStatus(**order_status), app.logger)

                else:
                    order = OrderStatus.query.filter_by(status='new', **previous_order).first()

                    if order:
                        order.status = 'canceled'
                        order.updated_at = order_status['updated_at']
                    else:
                        app.logger.warn('Unable to load row: {}'.format(order_status))

                db.session.commit()

        return redirect(url_for('uploaded_file', filename=filename))


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return render_template("upload_file.html")


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
