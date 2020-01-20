# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from webcolors import name_to_hex


class RainbowsPipeline(object):
    def process_item(self, item, spider):
        # All posts that don't count towards the rainbow
        invalid_post_ids = ["p256339",
                            "p256566",
                            "p256597",
                            "p256609",
                            "p256654",
                            "p256789",
                            "p258511",
                            "p258514",
                            "p258695",
                            "p259234",
                            "p268201",
                            "p270818",
                            "p276398",
                            "p282433",
                            "p282559",
                            "p282585",
                            "p290612",
                            "p311725",
                            "p376516",
                            "p377948",
                            "p383208",
                            "p412717",
                            "p460826",
                            "p460894",
                            "p462858",
                            "p474985"]

        # All posts that post the wrong color
        wrong_color_ids = {"p256373": "#24becb",
                           "p266544": "#bd7632",
                           "p266646": "#d4ba39",
                           "p304499": "#00ff00",
                           "p376532": "#d5c834",
                           "p376564": "#00ff11",
                           "p377998": "#d7a530",
                           "p378005": "#d7b84a",
                           "p462868": "#df7542",
                           "p462900": "#d3d258",
                           "p462956": "#c1f99f"}

        # All posts that have multiple colors in them
        multiple_colors_ids = {"p256374": "#822bae",
                               "p256572": "#b0b40e",
                               "p256932": "#c7902c",
                               "p257229": "#e7a256",
                               "p257233": "#eef7fa",
                               "p257570": "#65398d",
                               "p266777": "#edf825",
                               "p268076": "#cd6361",
                               "p271135": "#1b8202",
                               "p290675": "#fab854",
                               "p376531": "#ce933b",
                               "p378050": "#c182f3",
                               "p434270": "#8694c7"}

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
            item["color"] = item["color"].css("div[class='postmsg'] span::attr(style)")[0].get().lower()
            item["color"] = item["color"].replace("color: ", "")
            if not item["color"].startswith("#"):
                item["color"] = name_to_hex(item["color"])
        return item
