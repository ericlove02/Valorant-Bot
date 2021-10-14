from icrawler.builtin import BingImageCrawler
classes = ['valorant agents', 'valorant characters', 'valorant agents gameplay']
number = 200
for c in classes:
    bing_crawler = BingImageCrawler(storage={'root_dir': f'positive/{c.replace(" ", ".")}'})
    bing_crawler.crawl(keyword=c, filters=None, max_num=number, offset=0)
