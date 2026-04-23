#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书数据爬取服务
合法合规地爬取小红书公开数据
"""

import time
import random
import json
import re
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import concurrent.futures

app = Flask(__name__)

# 配置
CONFIG = {
    'MAX_WORKERS': 5,  # 最大并发数
    'REQUEST_INTERVAL': 2,  # 请求间隔（秒）
    'USER_AGENTS': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1'
    ],
    'REFERER': 'https://www.xiaohongshu.com/',
    'BASE_URL': 'https://www.xiaohongshu.com'
}

# 缓存
cache = {}
cache_expiry = {}

# 工具函数
def get_random_user_agent():
    """获取随机用户代理"""
    return random.choice(CONFIG['USER_AGENTS'])

def is_cache_valid(key):
    """检查缓存是否有效"""
    if key not in cache or key not in cache_expiry:
        return False
    return datetime.now().timestamp() < cache_expiry[key]

def set_cache(key, data, expiry=24*60*60):
    """设置缓存"""
    cache[key] = data
    cache_expiry[key] = datetime.now().timestamp() + expiry

def get_cache(key):
    """获取缓存"""
    if is_cache_valid(key):
        return cache[key]
    return None

def extract_tags(text):
    """提取文本中的标签"""
    tags = re.findall(r'#([^#\s]+)', text)
    return tags

def crawl_note_detail(note_id):
    """爬取笔记详情"""
    url = f"{CONFIG['BASE_URL']}/explore/{note_id}"
    headers = {
        'User-Agent': get_random_user_agent(),
        'Referer': CONFIG['REFERER']
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取笔记数据
        note_data = {
            'id': note_id,
            'title': '',
            'content': '',
            'likes': 0,
            'collections': 0,
            'comments': 0,
            'tags': [],
            'cover': '',
            'author': '',
            'type': 'image'  # 默认类型
        }
        
        # 提取标题
        title_elem = soup.find('h1', class_='title')
        if title_elem:
            note_data['title'] = title_elem.text.strip()
        
        # 提取内容
        content_elem = soup.find('div', class_='content')
        if content_elem:
            note_data['content'] = content_elem.text.strip()
            note_data['tags'] = extract_tags(note_data['content'])
        
        # 提取互动数据
        stats_elem = soup.find_all('span', class_='stats')
        if len(stats_elem) >= 3:
            note_data['likes'] = int(stats_elem[0].text.strip()) if stats_elem[0].text.strip().isdigit() else 0
            note_data['collections'] = int(stats_elem[1].text.strip()) if stats_elem[1].text.strip().isdigit() else 0
            note_data['comments'] = int(stats_elem[2].text.strip()) if stats_elem[2].text.strip().isdigit() else 0
        
        # 提取封面图
        cover_elem = soup.find('img', class_='cover')
        if cover_elem and cover_elem.get('src'):
            note_data['cover'] = cover_elem['src']
        
        # 提取作者
        author_elem = soup.find('span', class_='author')
        if author_elem:
            note_data['author'] = author_elem.text.strip()
        
        return note_data
    except Exception as e:
        print(f"爬取笔记 {note_id} 失败: {e}")
        return None

def search_notes(keywords, period=7, count=50):
    """搜索笔记"""
    # 构建缓存键
    cache_key = f"search_{'_'.join(keywords)}_{period}_{count}"
    
    # 检查缓存
    cached_result = get_cache(cache_key)
    if cached_result:
        return cached_result
    
    # 模拟搜索结果（实际项目中需要实现真实的搜索逻辑）
    # 这里使用模拟数据来演示，实际项目中需要根据关键词搜索小红书
    notes = []
    
    # 生成模拟的笔记ID
    for i in range(count):
        note_id = f"note_{random.randint(1000000, 9999999)}"
        note = crawl_note_detail(note_id)
        if note:
            notes.append(note)
        # 随机间隔，避免被封禁
        time.sleep(random.uniform(0.5, 2))
    
    # 处理数据格式，适配前端需求
    formatted_notes = []
    for note in notes:
        formatted_notes.append({
            'id': note['id'],
            'xsecToken': f"token_{note['id']}",
            'noteCard': {
                'type': note['type'],
                'displayTitle': note['title'],
                'user': {'nickname': note['author']},
                'interactInfo': {
                    'likedCount': note['likes'],
                    'collectedCount': note['collections'],
                    'commentCount': note['comments']
                },
                'cover': {'urlDefault': note['cover']}
            }
        })
    
    # 缓存结果
    set_cache(cache_key, formatted_notes)
    
    return formatted_notes

# API接口
@app.route('/api/v1/feeds/search', methods=['POST'])
def search_feeds():
    """搜索 feeds API"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', ['文创冰箱贴'])
        period = data.get('period', 7)
        count = data.get('count', 50)
        
        # 搜索笔记
        feeds = search_notes(keywords, period, count)
        
        return jsonify({
            'success': True,
            'feeds': feeds
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18060, debug=True)