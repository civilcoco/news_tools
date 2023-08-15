from NewsScraper import NewsScraper
from GUI_CREATE import NewsGUI

# 创建一个停用词列表
stopwords = ["新闻","邮箱","网易","新浪","视频","公司","专家","电影","游戏","国际","世界","亮相","媒体","客户端","事件","全国","财经","时尚","汽车","资讯"]

urls = ['https://news.163.com/', "https://news.sina.com.cn/"]
scraper = NewsScraper(urls,stopwords)
gui = NewsGUI(scraper)
gui.create_gui()

