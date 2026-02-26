# digest.py
import os
import json
import yaml
import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_rss(url, headers=None):
    try:
        feed = feedparser.parse(url, request_headers=headers or {})
        items = []
        for entry in feed.entries[:10]:
            title = entry.get('title', '')
            link = entry.get('link', '')
            if title and len(title) >= 5:
                items.append({'title': title, 'link': link})
        return items
    except Exception as e:
        print(f"RSS Error: {e}")
        return []

def fetch_html(url, selector):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = []
        for elem in soup.select(selector):
            title = elem.get_text().strip()
            link = elem.get('href', '')
            if link and not link.startswith('http'):
                link = urljoin(url, link)
            if title and len(title) >= 10:
                items.append({'title': title, 'link': link})
        return items
    except Exception as e:
        print(f"HTML Error: {e}")
        return []

def main():
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    all_news = []
    for source in config['sources']:
        print(f"Fetching from {source['name']}...")
        if source['type'] == 'rss':
            items = fetch_rss(source['url'], source.get('headers'))
        elif source['type'] == 'html':
            items = fetch_html(source['url'], source['selector'])
        else:
            continue
        
        for item in items:
            all_news.append({
                'title': item['title'],
                'link': item['link'],
                'source': source['name']
            })
    
    # 去重（简单标题去重）
    seen = set()
    unique_news = []
    for n in all_news:
        key = n['title'].lower().strip()
        if key not in seen and len(n['title']) >= config['fetch']['min_content_length']:
            seen.add(key)
            unique_news.append(n)
    
    # 限制总数
    unique_news = unique_news[:config['fetch']['max_items_total']]
    
    # 保存原始数据
    os.makedirs('output', exist_ok=True)
    with open(config['output']['raw_news_path'], 'w') as f:
        json.dump(unique_news, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Fetched {len(unique_news)} items")

if __name__ == '__main__':
    main()
