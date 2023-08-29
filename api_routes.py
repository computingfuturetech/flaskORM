from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from model import Customer,db,Product,Customer_orders
from werkzeug.utils import secure_filename
import os,json,secrets
from datetime import datetime

app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(app.root_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
db = SQLAlchemy(app)

@app.route('/createCustomer', methods=['POST'])
def createCustomer():
        try:
            customer_name = request.form.get('customer_name')
            email = request.form.get('email')
            address = request.form.get('address')
            total_orders =request.form.get('total_orders')
            new_customer = Customer(customer_name=customer_name, email=email, address=address, total_orders=total_orders)
            db.session.add(new_customer)
            db.session.commit()
            return jsonify({'message': 'Customer created successfully'}), 201 
        
        except Exception as e:

            return jsonify({'error': str(e)}), 400

@app.route('/getCustomerById/<int:id>',methods=['GET'])
def getCustomerById(id):
    try:
        session = db.session
        customer = session.query(Customer).get(id)

        if customer:
            customer_data = {
                'customer_id':customer.id,
                'customer_name': customer.customer_name,
                'email': customer.email,
                'address': customer.address,
                'total_orders': customer.total_orders
            }
            return jsonify(customer_data), 200
        else:
            return jsonify({'error': 'Customer not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
     
@app.route('/getAllCustomer',methods=['GET'])
def getAllCustomer():
    try:
        session = db.session
        customers = session.query(Customer).all()
        customer_data_list=[]
        for customer in customers:
            customer_data = {
                'customer_id':customer.id,
                'customer_name': customer.customer_name,
                'email': customer.email,
                'address': customer.address,
                'total_orders': customer.total_orders
            }
            customer_data_list.append(customer_data) 
        return jsonify(customer_data_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deleteCustomer/<int:id>',methods=['DELETE'])
def deleteCustomer(id):
    try:
        session = db.session
        customer=session.query(Customer).get(id)
        if customer:
            session.delete(customer)
            session.commit()
            return jsonify({'message':'Customer deleted successfully'}),200
        else:
            return jsonify({'error':'Customer not found'}),404
        
    except Exception as e:
        return jsonify({'error':str(e)}),500
    

@app.route('/updateCustomer/<int:id>',methods=['PUT'])
def updateCustomer(id):
    try:
        session = db.session
        customer=session.query(Customer).get(id)
        if not customer:
            return jsonify({'error':'Customer not found'})
        update_data = {
            'customer_name': request.form.get('customer_name'),
            'email': request.form.get('email'),
            'address': request.form.get('address'),
            'total_orders': request.form.get('total_orders')
        }
        for key, value in update_data.items():
            if value is not None:
                setattr(customer, key, value)

        session.commit()
        return jsonify({'message':'Customer data updated successfully'})
    
    except Exception as e:
        return jsonify({'error':str(e)}),500


UPLOAD_FOLDER='static\images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def generate_random_filename(filename):
    _, extension = os.path.splitext(filename)
    random_hex = secrets.token_hex(8)
    new_filename = random_hex + extension
    return new_filename

@app.route('/createProduct',methods=['POST'])
def createProduct():
    try:
        product_name=request.form.get('product_name')
        product_price=request.form.get('product_price')
        product_color=request.form.get('product_color')
        product_image=request.files.get('product_image')
        print(product_image)
        if not allowed_file(product_image.filename):
           return jsonify({'error':'Unsupported image data'}),400
        
        filename = secure_filename(product_image.filename)
        fn=generate_random_filename(filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'],fn)
        print(image_path)
        new_product=Product(product_name=product_name,product_price=product_price,product_color=product_color,product_image=image_path)
        session=db.session
        session.add(new_product)
        product_image.save(image_path)
        session.commit()
        return jsonify({'message':'Product created successfully'}),201
    
    except Exception as e:
        return jsonify({'error':str(e)}),500


@app.route('/getAllProduct',methods=['GET'])
def getAllProduct():
    try:
        session=db.session
        products = session.query(Product).all()
        product_data_list=[]
        for product in products:
            product_data = {
                'product_id':product.product_id,
                'product_name': product.product_name,
                'product_price':product.product_price,
                'product_color':product.product_color,
                'product_image':product.product_image
            }
            product_data_list.append(product_data) 
        return jsonify(product_data_list), 200
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/getProductById/<int:id>',methods=['GET'])
def getProductById(id):
    try:
        session = db.session
        product = session.query(Product).get(id)

        if product:
                product_data={
                'product_id':product.product_id,
                'product_name': product.product_name,
                'product_price':product.product_price,
                'product_color':product.product_color,
                }
                return jsonify(product_data)
        else:
            return jsonify({'message':'Prouct not found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deleteProduct/<int:product_id>',methods=['DELETE'])
def deleteProduct(product_id):
    try:
        session=db.session
        prod = session.get(Product,product_id)
        if prod:
            filename= prod.product_image
            os.remove(filename)
            session.delete(prod)
            session.commit()
            return jsonify({'message':'Product Delete successfully'})
        else:
            return jsonify({'error':'Product not found'})
    
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/updateProduct/<int:product_id>',methods=['PUT'])
def updateProduct(product_id):
    try:
        session=db.session
        product = session.get(Product,product_id)
        if not product:
           return jsonify({'error':'Product not found'})
        update_data={
            'product_name':request.form.get('product_name'),
            'product_price':request.form.get('product_price'),
            'product_color':request.form.get('product_color'),
            'product_image':request.files.get('product_image')
        }

        if 'product_image' in request.files:
            image_file = request.files['product_image']
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                fn = generate_random_filename(filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], fn)
                image_file.save(image_path)
                update_data['product_image'] = image_path

        for key, value in update_data.items():
            print(value)
            if value is not None:
                setattr(product, key, value)
            session.commit()
            return jsonify({'message':'product updated successfully'})
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/createOrder',methods=['POST'])
def createOrder():
    try:
        customer_id=request.form.get('customer_id')
        product_id=request.form.get('product_id')
        session = db.session
        customer = session.query(Customer).get(customer_id)
        session = db.session
        product = session.query(Product).get(product_id)
        if customer is None or product is None:
            return jsonify({'error':'customer or product is not found'})
        price=request.form.get('price')
        date_of_purchase_str = request.form.get('date_of_purchase')
        date_format_in_request = '%Y-%m-%d'
        date_of_purchase = datetime.strptime(date_of_purchase_str, date_format_in_request).date()
        total_paid=request.form.get('total_paid')
        order_status_str = request.form.get('order_status')
        order_status = bool(order_status_str.lower() == 'true')
        new_order=Customer_orders(customer_id=customer_id,product_id=product_id,price=price,date_of_purchase=date_of_purchase,total_paid=total_paid,order_status=order_status)
        session=db.session
        session.add(new_order)
        session.commit()
        return jsonify({'message':'Order placed successfully'})
    except Exception as e:
        return jsonify({'error':str(e)})
    
@app.route('/getAllOrder',methods=['GET'])
def getAllOrder():
    try:
        session=db.session
        orders=session.query(Customer_orders).all()
        list_of_order=[]
        for order in orders:
            order_data={
                'order_id':order.order_id,
                'customer_id':order.customer_id,
                'product_id':order.product_id,
                'price':order.price,
                'date_of_purchase': order.date_of_purchase.strftime('%Y-%m-%d'),
                'total_paid':order.total_paid,
                'order_status':order.order_status
            }
            list_of_order.append(order_data)
        return jsonify(list_of_order),200
    except Exception as e:
        return jsonify({'error':str(e)}),500

@app.route('/getOrdersByCustomerId/<int:customer_id>', methods=['GET'])
def getOrdersByCustomerId(customer_id):
    try:
        session=db.session
        customer_orders = session.query(Customer_orders).filter_by(customer_id=customer_id).all()
        
        if not customer_orders:
            return jsonify({'error':'customer order is not found'})

        customer_orders_list = []
        for order in customer_orders:
            order_dict = {
                'order_id': order.order_id,
                'product_id': order.product_id,
                'price': order.price,
                'date_of_purchase': order.date_of_purchase.strftime('%Y-%m-%d'),
                'total_paid': order.total_paid,
                'order_status': order.order_status
            }
            customer_orders_list.append(order_dict)

        return jsonify({'customer_orders': customer_orders_list})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/updateCustomerOrder/<int:order_id>',methods=['PUT'])
def updateCustomerOrder(order_id):
    try:
        session = db.session
        order = session.query(Customer_orders).get(order_id)

        if not order:
            return jsonify({'error': 'Order not found'})

        update_data = {
            'customer_id': request.form.get('customer_id'),
            'product_id': request.form.get('product_id'),
            'price': request.form.get('price'),
            'date_of_purchase': datetime.strptime(request.form.get('date_of_purchase'), '%Y-%m-%d').date(),
            'total_paid':request.form.get('total_paid'),
            'order_status': bool(request.form.get('order_status').lower() == 'true')
        }
        for key, value in update_data.items():
            if value is not None:
                setattr(order, key, value)
        session.commit()
        return jsonify({'message': 'Customer order data updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
   app.run(debug=True)

