# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from webcolors import name_to_hex

import json


class RainbowsPipeline(object):
    def process_item(self, item, spider):
        # All posts that don't count towards the rainbow
        with open("invalid.json", "r") as invalid:
            invalid_post_ids = json.load(invalid)

        # All posts that post the wrong color
        with open("wrong_color.json", "r") as wrong_color:
            wrong_color_ids = json.load(wrong_color)

        # All posts that have multiple colors in them
        with open("multiple_colors.json", "r") as multiple_colors:
            multiple_colors_ids = json.load(multiple_colors)

        if item["post_id"] in invalid_post_ids:
            # If a post does not count towards the rainbow
            raise DropItem(f"{item['post_id']} does not count towards the rainbow")
        elif item["post_id"] in list(wrong_color_ids.keys()):
            # If a post contains the wrong color
            item["color"] = wrong_color_ids[item["post_id"]]
        elif item["post_id"] in list(multiple_colors_ids.keys()):
            # IF a post contains multiple colors
            item["color"] = multiple_colors_ids[item["post_id"]]
        else:
            # Get the color that the user posted
            item["color"] = (
                item["color"]
                .css("div[class='postmsg'] span::attr(style)")[0]
                .get()
                .lower()
            )
            item["color"] = item["color"].replace("color: ", "")
            if not item["color"].startswith("#"):
                item["color"] = name_to_hex(item["color"])
        return item
