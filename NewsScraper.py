import requests
import jieba.posseg as pseg
from bs4 import BeautifulSoup
from collections import Counter

class NewsScraper:
    def __init__(self, urls , stopwords=None):
        self.urls = urls
        self.stopwords = stopwords if stopwords is not None else []
        self.news = self.scrape_news_titles()
        self.whitelist = ["高考","无人机"]  # 添加白名单

    # 消除停用词
    def remove_stopwords(self, text):
        for word in self.stopwords:
            text = text.replace(word, "")
        return text

    # 获取新闻标题
    def scrape_news_titles(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        news = {}
        for url in self.urls:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'  # 添加这行代码指定字符编码
            soup = BeautifulSoup(response.text, 'html.parser')

            if "163.com" in url:
                divs = soup.find_all('div')
                for div in divs:
                    a = div.find('a')
                    if a is not None:
                        href = a.get('href')
                        title = a.text.strip()
                        if href and href != "https://open.163.com/" and href != "javascript:;" and title:
                            news[title] = href

            elif "sina.com.cn" in url:
                as_ = soup.find_all('a')  # 直接找到所有的 'a' 标签
                for a in as_:
                    href = a.get('href')
                    title = a.text.strip()
                    if href and title and 'sina.com.cn' in href:  # 这里添加了一个过滤条件，只有包含 'sina.com.cn' 的链接才被接受
                        news[title] = href

        return news

    def search_news(self, keyword):
        # 进行搜索
        search_results = {title: href for title, href in self.news.items() if keyword.lower() in title.lower()}

        return search_results

    def get_hot_topics(self, top_n, min_length=4):
        # 对每一条新闻标题进行关键词提取
        # pseg.cut(title)将会返回一个元组列表，元组的第一个元素是词，第二个元素是词性。flag.startswith('n')将会检查词性是否以'n'开始，代表名词或专有名词。
        # 在关键词提取条件中加入白名单判断
        keywords_lists = [[word for word, flag in pseg.cut(self.remove_stopwords(title)) if
                           flag.startswith('n') or word in self.whitelist] for title in self.news.keys()]

        # 将所有的关键词列表合并，并且只保留长度大于或等于阈值且不包含数字的关键词
        all_keywords = [keyword for keywords in keywords_lists for keyword in keywords
                        if len(keyword) >= min_length and not any(char.isdigit() for char in keyword)]

        # 统计每个词出现的频率
        word_counts = Counter(all_keywords)

        # 返回最常出现的top_n个词
        return word_counts.most_common(top_n)

    def fetch_image(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_url = None  # 初始化为 None

        if "163.com" in url:
            p = soup.find('p', class_='f_center')
            if p is not None:
                img = p.find('img')
                if img is not None:
                    image_url = img['src']

        elif "sina.com.cn" in url:
            div_img = soup.select_one('#article > div:nth-child(4) > img')
            if div_img:
                image_url = div_img['src']
                if image_url.startswith("//"):
                    image_url = "https:" + image_url

        # 获取图片内容
        response = requests.get(image_url, headers=headers)

        # 检查响应状态
        if response.status_code != 200:
            print(f"Failed to fetch the image. Status code: {response.status_code}")
            return None

        # 返回图片的二进制数据
        return response.content

    def fetch_image_links(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        image_links = []

        if "163.com" in url:
            imgs = soup.find_all('img', src=True)
            for img in imgs:
                image_links.append(img['src'])

        elif "sina.com.cn" in url:
            imgs = soup.select('#article img')
            for img in imgs:
                src = img['src']
                if src.startswith("//"):
                    src = "https:" + src
                image_links.append(src)

        return image_links

    def fetch_image_single(self, image_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

        # 如果图片URL以"//"开头，添加"https:"
        if image_url.startswith("//"):
            image_url = "https:" + image_url

        # 获取图片内容
        response = requests.get(image_url, headers=headers)

        # 检查响应状态
        if response.status_code != 200:
            print(f"Failed to fetch the image. Status code: {response.status_code}")
            return None

        # 返回图片的二进制数据
        return response.content





