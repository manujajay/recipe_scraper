from flask import Flask, render_template, request, session, url_for, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        ingredients = scrape_ingredients(url)
        return render_template('index.html', ingredients=ingredients)
    return render_template('index.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        item = request.form['item']
        if 'cart_items' not in session:
            session['cart_items'] = []
        session['cart_items'].append(item)
        session.modified = True
        return redirect(url_for('cart'))

    cart_items = session.get('cart_items', [])
    return render_template('cart.html', cart=cart_items)

def scrape_ingredients(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    ingredients_container = soup.find('section', class_='recipe__ingredients')

    if not ingredients_container:
        return []

    ingredients = []
    for li in ingredients_container.find_all('li', class_='list-item'):
        ingredient_text = ' '.join(li.stripped_strings)
        if ingredient_text:
            ingredients.append(ingredient_text)

    return ingredients

@app.route('/cart/count', methods=['GET'])
def cart_count():
    cart_items = session.get('cart_items', [])
    return str(len(cart_items))

@app.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    item = request.form['item']
    cart_items = session.get('cart_items', [])
    if item in cart_items:
        cart_items.remove(item)
        session.modified = True
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
