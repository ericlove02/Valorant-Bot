from icrawler.builtin import GoogleImageCrawler
classes = ['valorant agents character models']
number = 100
# classes = ['valorant maps']
# number = 300
for c in classes:
    crawler = GoogleImageCrawler(storage={'root_dir': f'cascadedata/p2/'})
    # bing_crawler = BingImageCrawler(storage={'root_dir': f'negative/)
    crawler.crawl(keyword=c, filters=None, max_num=number, offset=0)
