import scrapy

from rainbows.items import RainbowPost


class RainbowSpider(scrapy.Spider):
    name = "rainbows"
    start_urls = [
        "https://tbgforums.com/forums/viewtopic.php?id=2956"
    ]

    def parse(self, response):
        for post in response.css(".blockpost"):
            item = RainbowPost()

            item["author"] = post.css("dl > dt > strong::text")[0].get()
            item["color"] = post.css("div.postright > div:nth-child(2)")[0]
            item["post_id"] = post.css("div.blockpost::attr(id)")[0].get()

            yield item

        next_page = response.css('div.pagepost > p > a[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
