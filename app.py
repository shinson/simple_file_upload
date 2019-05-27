import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename


# CONFIG
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['tsv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/purchase_log'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# MODELS
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    fist_name = db.Column(db.Text, nullable=False)
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

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    price = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum("new", "cancel", name="order_enum", create_type=False))
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

        file = request.files['file']

        if file.filename == '':
            flash('Invalid file!')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return render_template("upload_file.html")


if __name__ == '__main__':
    app.run(debug=True)
