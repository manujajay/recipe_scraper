from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        ingredients = scrape_ingredients(url)
        return render_template('index.html', ingredients=ingredients)
    return render_template('index.html')

def scrape_ingredients(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the ingredients container
    ingredients_container = soup.find('ul', class_='list')

    if not ingredients_container:
        return []

    # Extract ingredients and quantities from the container
    ingredients = []
    for li in ingredients_container.find_all('li', class_='list-item'):
        # Combine the text of all child elements
        ingredient_text = ' '.join([child.text for child in li.contents if child.string])
        ingredient_text = ingredient_text.strip()
        if ingredient_text:
            ingredients.append(ingredient_text)

    return ingredients


if __name__ == '__main__':
    app.run(debug=True)
