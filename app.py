from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask app is running!"

@app.route('/scrape', methods=['GET'])
def scrape():
    print("Request received to /scrape")
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        article_div = soup.find('div', {'class': 'article-content'})
        if not article_div:
            article_div = soup.find('article') or soup.find('main', {'role': 'main'})
        if not article_div:
            return jsonify({'error': 'Article content not found'}), 404

        paragraphs = article_div.find_all('p')
        article_text = "\n\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())

        return jsonify({
            'text': article_text,
            'url': url
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
