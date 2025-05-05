from flask import Flask, render_template, request
from TP_1 import connect_mongodb
from datetime import datetime

app = Flask(__name__)

def search_articles_advanced(start_date=None, end_date=None, author=None, category=None, subcategory=None, title_search=None):
    collection = connect_mongodb()
    query = {}
    
    if start_date:
        query['date'] = {'$gte': start_date}
    if end_date:
        if 'date' in query:
            query['date']['$lte'] = end_date
        else:
            query['date'] = {'$lte': end_date}
    if author:
        query['author'] = author
    if category:
        query['category'] = category
    if subcategory:
        query['subcategory'] = subcategory
    if title_search:
        query['title'] = {'$regex': title_search, '$options': 'i'}
    
    return list(collection.find(query))

@app.route('/', methods=['GET', 'POST'])
def index():
    articles = []
    categories = []
    subcategories = []
    authors = []
    
    collection = connect_mongodb()
    categories = collection.distinct('category')
    subcategories = collection.distinct('subcategory')
    authors = collection.distinct('author')
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        author = request.form.get('author')
        category = request.form.get('category')
        subcategory = request.form.get('subcategory')
        title_search = request.form.get('title_search')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        
        articles = search_articles_advanced(
            start_date=start_date,
            end_date=end_date,
            author=author,
            category=category,
            subcategory=subcategory,
            title_search=title_search
        )
    
    return render_template('index.html', 
                         articles=articles,
                         categories=categories,
                         subcategories=subcategories,
                         authors=authors)

if __name__ == '__main__':
    app.run(debug=True) 