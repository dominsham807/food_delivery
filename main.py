from flask import Flask,render_template,send_from_directory,request,redirect,flash,url_for,session
from models import *
import random
from flask_uploads import configure_uploads,IMAGES,UploadSet,patch_request_class
from PIL import Image,ImageGrab
##from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_session import Session
##from sqlalchemy.sql import select
##from models import customers
##from sqlalchemy import create_engine
##from sqlalchemy.orm import sessionmaker
from flask_bootstrap import Bootstrap
from flask import send_from_directory
from flask_login import login_required
import os
from werkzeug.datastructures import CombinedMultiDict,MultiDict


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'

images = UploadSet('photos',IMAGES)
configure_uploads(app,images)
patch_request_class(app)

Session(app)
##POSTGRES = {
##    'user':'dominicsham807',
##    'pw':'996322',
##    'db':'food_delivery',
##    'host':'127.0.0.1',
##    'port':'5432',
##}
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ds996322'
app.config['MYSQL_DB'] = 'food_delivery'

mysql = MySQL(app)

Bootstrap(app)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    # Uncomment each of the following queries to create 5 tables on database
##    query = '''CREATE TABLE customers (
##                no INT AUTO_INCREMENT PRIMARY KEY,
##                name VARCHAR(50) NOT NULL,
##                username VARCHAR(100),
##                password VARCHAR(100),
##                tel INT,
##                email VARCHAR(100),
##                member BOOLEAN)'''
##    query = '''CREATE TABLE order_receipts (
##                name VARCHAR(50) NOT NULL,
##                order_no INT,
##                items VARCHAR(350),
##                quantity INT,
##                price DECIMAL(5,1),
##                discount DECIMAL(5,2),
##                payment_method VARCHAR(50),
##                delivery_time TIME,
##                delivery_addr VARCHAR(200),
##                member BOOLEAN)'''
##    query = '''CREATE TABLE cuisines (
##                type VARCHAR(50),
##                restaurant VARCHAR(100),
##                item VARCHAR(100),
##                price INT,
##                img BLOB)'''
##    query = '''CREATE TABLE restaurants (
##                type VARCHAR(100),
##                restaurant VARCHAR(60),
##                address VARCHAR(200),
##                open_time TIME,
##                close_time TIME,
##                tel INT,
##                hotline INT)'''
##    query = '''CREATE TABLE staff (
##                no INT AUTO_INCREMENT PRIMARY KEY,
##                name VARCHAR(50) NOT NULL,
##                username VARCHAR(100),
##                password VARCHAR(100),
##                staff_id INT,
##                tel INT,
##                email VARCHAR(100))'''
####
##    query = "ALTER TABLE orders CHANGE order_time delivery_time TIME"
##    query = "DELETE FROM order_receipts WHERE name='Dominic'"
##    query = 'DROP TABLE customers'
    cursor.execute(query)
    mysql.connection.commit()
    cursor.close()
    return 'Table updated successfully'
            
    
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = CustomerRegister(request.form,meta={'csrf': False})
    if form.validate_on_submit():
        name = form.name.data
        mobile = form.mobile.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        member = form.member.data
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO customers(name,username,password,tel,email,member) VALUES(%s,%s,%s,%s,%s,%s)'
        values = (name,username,password,mobile,email,member)
        cursor.execute(query,values)
        mysql.connection.commit()
        cursor.close()
        return redirect('/login',code=302)
    return render_template('reg_account.html',form=form)

@app.route('/homepage_loggedin/<name>')
def homepage_loggedin(name):
    return render_template('homepage_loggedin.html',name=name)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForms(request.form)
##    staff_form = StaffForm(request.form,meta={'csrf': False})
##    admin_form = AdminForm(request.form,meta={'csrf': False})
    if request.method == 'POST' and form.validate():
        if request.form['btn'] == 'Login':
            username = form.username.data
            password = form.password.data
            cursor = mysql.connection.cursor()
            query1 = 'SELECT username,password FROM customers'
            cursor.execute(query1)
            datas = cursor.fetchall()
    ##        mysql.connection.commit()
            cursor.close()
            accounts = {}
            for x,y in datas:
                accounts[x] = y
            if username in accounts:
                if password == accounts[username]:
                    cursor = mysql.connection.cursor()
                    query2 = 'SELECT name FROM customers where username = %s'
                    cursor.execute(query2,(username,))
                    datas = cursor.fetchone()
                    cursor.close()
                    return redirect(url_for('homepage_loggedin',name=datas[0]))
                else:
                    error = 'Incorrect password!'
                    return render_template('loginPage.html',form=form,customer_error=error)
            else:
                error = 'Invalid username!'
                return render_template('loginPage.html',form=form,customer_error=error)

        elif request.form['btn'] == 'Enter':
            username = form.username.data
            password = form.password.data
            cursor = mysql.connection.cursor()
            query1 = 'SELECT username,password FROM staff'
            cursor.execute(query1)
            datas = cursor.fetchall()
            accounts = {}
            for x,y in datas:
                accounts[x] = y
            if username in accounts:
                if password == accounts[username]:
                    cursor = mysql.connection.cursor()
                    query2 = 'SELECT name FROM staff where username = %s'
                    cursor.execute(query2,(username,))
                    datas = cursor.fetchone()
                    cursor.close()
                    return redirect(url_for('staff_homepage',name=datas[0]))
                else:
                    error = 'Incorrect password!'
                    return render_template('loginPage.html',form=form,staff_error=error)
            else:
                error = 'Invalid username!'
                return render_template('loginPage.html',form=form,staff_error=error)

        elif request.form['btn'] == 'Submit':
            if form.username.data == 'admin@ufood':
                if form.password.data == 'Ds996322':
                    return redirect(url_for('admin_page'))
                else:
                    error = 'Incorrect password! Please try again!'
                    return render_template('loginPage.html',form=form,admin_error=error)
            else:
                error = 'Invalid data!'
                return render_template('loginPage.html',form=form,admin_error=error)

    return render_template('loginPage.html',form=form)

@app.route('/customer_orders/<name>',methods=['GET','POST'])
def customer_orders(name):
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM order_receipts WHERE name = %s'
    cursor.execute(query,(name,))
    ordered_items = cursor.fetchall()
##    print(ordered_items)
##    req_items = []
    products = []
    req_items = ordered_items[0][2].split(', ')
    for item in req_items:
        products.append(item)
##    print(products)
##    item_list = ordered_items[2].split(',')
    product_names = []
    quantities = []
    for item in products:
        product_names.append(item.split('*')[0])
        quantities.append(item.split('*')[1])
##    print(product_names)
    product_data = []
    i = 0
    for product in product_names:
        query2 = 'SELECT type,price,restaurant,img FROM cuisines WHERE item = %s'
        cursor.execute(query2,(product,))
        info = cursor.fetchall()
        product_info = {}
        product_info['type'] = info[0][0]
        product_info['item'] = product
        product_info['quantity'] = quantities[i]
        product_info['price'] = info[0][1]*int(product_info['quantity'])
##        print(product_info['quantity'])
##        print(type(product_info['quantity']))
        product_info['restaurant'] = info[0][2]
        product_info['image'] = info[0][3]
        product_data.append(product_info)
        i += 1
##    print(product_data)
    return render_template('customer_orders.html',order_num=ordered_items[0][1],name=name,product_data=product_data,ordered_items=ordered_items)

@app.route('/customers_products/<name>',methods=['GET','POST'])
def customers_products(name):
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM cuisines'
    cursor.execute(query)
    products = cursor.fetchall()
##    for product in products:
##        print(product[4].decode('utf-8'))
    session['total_amount'] = 0
    session['total_items'] = []
    session['quantity'] = 0
##    for product in products:
##    print(products)
    total_number = []
    if request.method == 'POST':
        order_numbers = [i for i in range(101,400)]
        cursor = mysql.connection.cursor()
        query = 'SELECT order_no FROM order_receipts'
        cursor.execute(query)
        numbers = cursor.fetchall()
    ##    print(numbers)
        numbers_used = []
        for number in numbers:
            numbers_used.append(number[0])
            order_numbers.remove(number[0])
    ##    print(order_numbers)
                
                
        order_num = random.randint(order_numbers[1],order_numbers[-1])
  
        session['num_arranged'] = order_num
        
        input_amount = request.form.getlist('amount')
        for amount in input_amount:
            req_amt = int(amount)
            total_number.append(req_amt)
##        print(input_amount)
        i = 0
        for product in products:
            input_prod = product[2]
            prod_amt = total_number[i]
##            prod_amt = int(prod_amt)
            if prod_amt == 0:
                req_amt += 0
            else:
                
                req_amt = prod_amt*product[3]
                session['total_amount'] += req_amt
                session['quantity'] += int(input_amount[i])
                session['total_items'].append(input_prod+'*'+str(prod_amt))
            i += 1
        
##        print(total_items)
##        print(len(total_items))
##        print(total_amount)
        cursor = mysql.connection.cursor()
        query = 'SELECT member FROM customers WHERE name = %s'
        cursor.execute(query,(name,))
        session['is_member'] = cursor.fetchone()[0]
##        print(type(session['is_member']))
        if session['is_member'] == 1:
            session['total_amount'] *= 0.8
            session['discount'] = 0.80
            session['is_member'] = 'Applied'
        else:
            session['discount'] = 0.00
            session['is_member'] = 'Non-member'
            
        return redirect(url_for('customer_payment',name=name))
    return render_template('customers_products.html',name=name,products=products)

@app.route('/customer_payment/<name>',methods=['GET','POST'])
def customer_payment(name):
##    print(order_num)
    if request.method == 'POST':
##        order_numbers = [i for i in range(101,400)]
        cursor = mysql.connection.cursor()
##        query = 'SELECT order_no FROM order_receipts'
##        cursor.execute(query)
##        numbers = cursor.fetchall()
##    ##    print(numbers)
##        numbers_used = []
##        for number in numbers:
##            numbers_used.append(number[0])
##            order_numbers.remove(number[0])
##    ##    print(order_numbers)
##            
##            
##    
    
        payment_method = request.form['pay_method']
        delivery_addr = request.form['address']
        delivery_time = request.form['time_to_deliver']
        
        if session.get('is_member') == 'Applied':
            item_list = ', '.join(session.get('total_items'))
            query = '''INSERT INTO order_receipts(name,order_no,items,quantity,price,discount,payment_method,delivery_time,delivery_addr,member)
                      VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)  '''
            values = (name,session.get('num_arranged'),item_list,session.get('quantity'),
                      session.get('total_amount'),session.get('discount'),payment_method,delivery_time,delivery_addr,True)
            cursor.execute(query,values)
            mysql.connection.commit()
        else:
            item_list = ', '.join(session.get('total_items'))
            query = '''INSERT INTO order_receipts(name,order_no,items,quantity,price,discount,payment_method,delivery_time,delivery_addr,member)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            values = (name,session.get('num_arranged'),item_list,session.get('quantity'),
                      session.get('total_amount'),0.0,payment_method,delivery_time,delivery_addr,False)
            cursor.execute(query,values)
            mysql.connection.commit()
        return redirect(url_for('customer_orders',name=name))
    return render_template('customer_payment.html',name=name,order_num=session.get('num_arranged'),discount=session.get('discount'),
                quantity=session.get('quantity'),total_items=session.get('total_items'),
                    total_amount=session.get('total_amount'),member=session.get('is_member'))

@app.route('/customers_restaurants/<name>')
def customers_restaurants(name):
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM restaurants'
    cursor.execute(query)
    restaurants = cursor.fetchall()
    return render_template('customers_restaurants.html',name=name,restaurants=restaurants)

@app.route('/admin_page')
def admin_page():
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM customers'
    cursor.execute(query)
    datas = cursor.fetchall()
    cursor.close()
##    datas = list(datas)
    for data in datas:
        is_member = data[5]
        if is_member == '0':
            is_member = 'Non-member'
        else:
            is_member = 'Member'
    return render_template('admin_page.html',datas=datas)
  
@app.route('/view_customer/<index>',methods=['GET','POST'])
def view_customer(index):
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM customers WHERE no = %s'
    cursor.execute(query,(index,))
    datas = cursor.fetchone()
    cursor.close()
    name = datas[1]
##    username = datas[2]
##    password = datas[3]
    mobile = datas[4]
    email = datas[5]
    member = datas[6]
    return render_template('view_customer.html',index=index,name=name,
                           mobile=mobile,email=email,is_member=member)

@app.route('/staff_crud')
def staff_crud():
    cursor = mysql.connection.cursor()
    query = 'SELECT * FROM staff'
    cursor.execute(query)
    datas = cursor.fetchall()
    cursor.close()
    return render_template('staff_crud.html',datas=datas)


@app.route('/add_staff',methods=['GET','POST'])
def add_staff():
    form = StaffForm(request.form,meta={'csrf': False})
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password = form.password.data
        staff_id = form.staff_id.data
        mobile = form.mobile.data
        email = form.email.data
##        duty = form.duty.data
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO staff(name,username,password,staff_id,tel,email) VALUES(%s,%s,%s,%s,%s,%s)'
        values = (name,username,password,staff_id,mobile,email)
        cursor.execute(query,values)
        mysql.connection.commit()
        cursor.close()
        return redirect('/staff_crud',code=302)
    return render_template('add_staff.html',form=form)

@app.route('/staff_homepage/<name>')
def staff_homepage(name):
    cursor = mysql.connection.cursor()
    query = 'SELECT staff_id,tel,email FROM staff WHERE name = %s'
    cursor.execute(query,(name,))
    datas = cursor.fetchone()
    staff_id = datas[0]
    mobile = datas[1]
    email = datas[2]
##    duty = datas[3]
    return render_template('staff_homepage.html',name=name,staff_id=staff_id,mobile=mobile,email=email)

@app.route('/products/<name>')
def products(name):
    cursor = mysql.connection.cursor()
    query = 'SELECT * from cuisines'
    cursor.execute(query)
    datas = cursor.fetchall()

##    for data in datas:
##        cuisine_img = data[3].decode('utf-8')

    return render_template('products.html',name=name,datas=datas)

@app.route('/product_add/<name>',methods=['GET','POST'])
def product_add(name):
    
    form = Products(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        item = form.item.data
        cuisine_type = form.cuisine_type.data
        restaurant_select = form.restaurant.data
        price = form.price.data
        filename = images.save(form.image.data)
        file_url = images.url(filename)
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO cuisines(type,restaurant,item,price,img) VALUES(%s,%s,%s,%s,%s)'
        values = (cuisine_type,restaurant_select,item,price,filename)
        cursor.execute(query,values)
        mysql.connection.commit()
        cursor.close()
##        return 'Success'
        return redirect(url_for('products',name=name,filename=filename))
    return render_template('product_add.html',name=name,form=form)
    
@app.route('/restaurants/<name>')
def restaurants(name):
    cursor = mysql.connection.cursor()
    query = 'SELECT * from restaurants'
    cursor.execute(query)
    datas = cursor.fetchall()
##    print(datas)
##    os.chdir('F:\Web\Food Delivery App\photos')
    return render_template('restaurants.html',datas=datas,name=name)

@app.route('/add_restaurant/<name>',methods=['GET','POST'])
def add_restaurant(name):
    form = Restaurants(request.form,meta={'csrf': False})
    if form.validate_on_submit():
        restaurant_name = form.name.data
        cuisine_type = form.cuisine_type.data
        address = form.address.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        tel = form.tel.data
        hotline = form.hotline.data
        cursor = mysql.connection.cursor()
        query = 'INSERT INTO restaurants(type,restaurant,address,open_time,close_time,tel,hotline) VALUES(%s,%s,%s,%s,%s,%s,%s)'
        values = (cuisine_type,restaurant_name,address,str(open_time),str(close_time),tel,hotline)
        cursor.execute(query,values)
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('restaurants',name=name))
    
    return render_template('add_restaurant.html',form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('homepage'))





if __name__ == '__main__':
    app.run(use_reloader=False,debug=True)
