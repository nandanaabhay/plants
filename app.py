from flask import Flask, render_template ,request, redirect , url_for
from plants_data import plants  

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
