# -*- coding: utf-8 -*-

# Scrapy settings for rainbows project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'rainbows'

SPIDER_MODULES = ['rainbows.spiders']
NEWSPIDER_MODULE = 'rainbows.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'rainbows.pipelines.RainbowsPipeline': 300,
}
