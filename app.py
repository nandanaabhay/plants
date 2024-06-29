from flask import Flask, render_template ,request, redirect , url_for
from plants_data import plants 
#-----------------------------------------------------BELOW------------------------------------------------------------------
#TODO: Download & Install MySQL
#TODO: pip install Flask-MySQLdb
#TODO: Add your password in ''
#TODO: Confirm if MySQL is running
#   -> Press windows + R
#   -> Type: services.msc
#   -> Find: MySQL
#   -> Right click: Start
#TODO: Go to MySQL command line and run:
#   -> mysql -u root -p
#   -> Enter password
#   -> CREATE DATABASE plants_db;
#   -> EXIT;
#TODO: Add '/view_orders' after your localhost url to view orders
#-----------------------------------------------------ABOVE------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------
from flask_mysqldb import MySQL
#-----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)

#-----------------------------------------------------------------------------------------------------------------------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Stroberri1.'
app.config['MYSQL_DB'] = 'plants_db'

mysql = MySQL(app)

with app.app_context():

    def create_table():
        # Establish a database connection
        cursor = mysql.connection.cursor()

        # SQL query to create a new table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            plant_name VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            delivery_address TEXT NOT NULL,
            phone_number VARCHAR(15) NOT NULL
        )
        '''
        
        # Execute the SQL command
        cursor.execute(create_table_query)

        # Commit the changes
        mysql.connection.commit()

        # Close the cursor
        cursor.close()

        print("Table created successfully!")
#-----------------------------------------------------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html', success=False)

@app.route('/products')
def products():
    return render_template('products.html', plants=plants)

@app.route('/plant_data')
def plant_data():
    return render_template('plants_data.html', plants=plants)

@app.route('/buy/<plant_name>', methods=['GET', 'POST'])
def buy(plant_name):
    plant = next((p for p in plants if p['name'] == plant_name), None)
    if request.method == 'POST':
        name = request.form['name']
        delivery_address = request.form['delivery_address']
        phone_number = request.form['phone_number']
        
#-----------------------------------------------------------------------------------------------------------------------
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO orders (plant_name, name, delivery_address, phone_number) VALUES (%s, %s, %s, %s) ''', (plant_name, name, delivery_address, phone_number))
        mysql.connection.commit()
        cursor.close()
#-----------------------------------------------------------------------------------------------------------------------
        
        print(f'Plant: {plant_name}, Name: {name}, Delivery Address: {delivery_address}, Phone Number: {phone_number}')
        return redirect(url_for('products'))
    return render_template('buy.html', plant=plant)

@app.route('/product/<plant_name>')
def product(plant_name):
    plant = next((p for p in plants if p['name'] == plant_name), None)
    if plant:
        return render_template('product.html', plant=plant)
    return 'Plant not found', 404

@app.route('/login')
def login():
    return render_template('login.html')

#-----------------------------------------------------------------------------------------------------------------------
@app.route('/view_orders')
def view_orders():
    # Fetch data from MySQL DATABASE
    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT * FROM orders ''')
    data = cursor.fetchall()
    cursor.close()

    return render_template('view_orders.html', orders=data)
#-----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
#-----------------------------------------------------------------------------------------------------------------------
    with app.app_context():
        #creates table if not existing
        create_table()
#-----------------------------------------------------------------------------------------------------------------------
    app.run(debug=True)
