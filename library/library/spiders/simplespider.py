import scrapy

class QuotesSpider(scrapy.Spider):
    name = "tacos"
    def start_requests(self):
        urls = [
            'https://books.toscrape.com/catalogue/page-1.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for book in response.xpath('//article'):
            yield {
                'name': book.xpath('.//a/@title').get(),
                'rating': book.xpath('.//p').attrib['class'],
                'price': book.xpath('.//div[2]/p/text()').get(),
                'stock': book.xpath('.//div[2]/p[2]/i/following-sibling::text()').get().strip()
            }
        next_page = response.css('.next a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)