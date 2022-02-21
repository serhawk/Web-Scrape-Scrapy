import scrapy
from ..items import LibraryItem


class CoverSpider(scrapy.Spider):
	name = "imagespider"

	def start_requests(self):
		urls = [
			'https://books.toscrape.com/catalogue/page-1.html',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for images in response.xpath('//article'):
			image = images.xpath('.//a/img/@src').get()
			imageURL=response.urljoin(image)
			yield LibraryItem(file_urls=[imageURL])
		next_page = response.css('.next a').attrib['href']
		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)

