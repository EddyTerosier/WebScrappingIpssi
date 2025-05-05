import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

def connect_mongodb():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['blog_moderateur']
    return db['articles']

# Fonction pour récupérer les détails d'un article
def get_article_details(article_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Récupération de la page de l'article
        response = requests.get(article_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Récupération de la catégorie
        category = None
        shadow_div = soup.find('div', class_='shadow-top')
        if shadow_div:
            container_div = shadow_div.find('div', class_='container-fluid')
            if container_div:
                category_links = container_div.find_all('a', class_='t-def')
                if len(category_links) >= 3:  # Le troisième lien contient la catégorie
                    category = category_links[2].text.strip()
        
        # Récupération de l'auteur et de la date
        meta_div = soup.find('div', class_='entry-meta article-meta d-flex')
        author = None
        date = None
        
        if meta_div:
            # Récupération de l'auteur
            byline = meta_div.find('span', class_='byline')
            if byline:
                author_link = byline.find('a')
                if author_link:
                    author = author_link.text.strip()
            
            # Récupération de la date
            posted_on = meta_div.find('span', class_='posted-on')
            if posted_on:
                time_tag = posted_on.find('time')
                if time_tag and 'datetime' in time_tag.attrs:
                    date = time_tag['datetime'].split('T')[0]
        
        # Récupération du contenu principal
        content = None
        content_div = soup.find('div', class_='entry-content')
        if content_div:
            # Récupération de tous les paragraphes
            paragraphs = content_div.find_all('p')
            if paragraphs:
                content = '\n'.join([p.text.strip() for p in paragraphs])
        
        # Récupération des images
        images = {}
        article_div = soup.find('article')
        if article_div:
            for img in article_div.find_all('img'):
                if 'src' in img.attrs and not img['src'].startswith('data:'):
                    alt_text = img['alt'] if 'alt' in img.attrs else ''
                    caption = img['title'] if 'title' in img.attrs else alt_text
                    images[img['src']] = caption
        
        return {
            'author': author,
            'date': date,
            'summary': content,
            'images': images,
            'category': category,
            'content': content
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des détails de l'article: {e}")
        return None

def fetch_articles(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Récupération des articles...")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Liste pour stocker les articles
        articles_data = []
        articles = soup.find_all('article')
        print(f"Nombre d'articles trouvés: {len(articles)}")
        
        for article in articles:
            try:
                # Récupération de l'URL et du titre
                header = article.find('header')
                a_tag = header.find('a') if header else None
                article_url = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None
                
                title_h3 = a_tag.find('h3') if a_tag else None
                title = title_h3.text.strip() if title_h3 else None
                if not title and a_tag:
                    title = a_tag.text.strip()
                
                # Récupération de la sous-catégorie
                meta_div = article.find('div', class_='entry-meta')
                tag_span = meta_div.find('span', class_='favtag color-b') if meta_div else None
                subcategory = tag_span.text.strip() if tag_span else None
                
                # Récupération de l'image
                img_div = article.find('div', class_='post-thumbnail')
                img_tag = img_div.find('img') if img_div else None
                thumbnail = None
                if img_tag:
                    if 'data-lazy-src' in img_tag.attrs:
                        thumbnail = img_tag['data-lazy-src']
                    elif 'src' in img_tag.attrs:
                        thumbnail = img_tag['src']
                
                # Récupération des détails de l'article
                article_details = None
                if article_url:
                    print(f"Récupération des détails pour: {title}")
                    article_details = get_article_details(article_url)
                
                # Création du dictionnaire de l'article
                article_data = {
                    'url': article_url,
                    'title': title,
                    'category': article_details['category'] if article_details else None,
                    'date': article_details['date'] if article_details else None,
                    'subcategory': subcategory,
                    'summary': article_details['summary'] if article_details else None,
                    'images': article_details['images'] if article_details else {},
                    'author': article_details['author'] if article_details else None,
                    'thumbnail': thumbnail,
                    'content': article_details['content'] if article_details else None
                }
                
                articles_data.append(article_data)
                print(f"Article ajouté: {title}")
                
            except Exception as e:
                print(f"Erreur lors du traitement d'un article: {e}")
                continue
        
        return articles_data
    
    except Exception as e:
        print(f"Erreur lors du scraping: {e}")
        return []

def save_to_mongodb(articles):
    collection = connect_mongodb()
    for article in articles:
        try:
            collection.update_one(
                {'url': article['url']},
                {'$set': article},
                upsert=True
            )
            print(f"Article sauvegardé: {article['title']}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")

def search_articles(category=None, subcategory=None):
    collection = connect_mongodb()
    query = {}
    
    if category:
        query['category'] = category
    if subcategory:
        query['subcategory'] = subcategory
    
    return list(collection.find(query))

# Programme principal
if __name__ == "__main__":
    url = "https://www.blogdumoderateur.com/"
    print("Début du scraping...")
    articles = fetch_articles(url)
    print(f"Nombre d'articles récupérés: {len(articles)}")
    
    if articles:
        print("Sauvegarde dans MongoDB...")
        save_to_mongodb(articles)
    
    # Affichage des articles
    for i, article in enumerate(articles, 1):
        print(f"\nArticle {i}:")
        for key, value in article.items():
            print(f"{key.capitalize()}: {value}")
