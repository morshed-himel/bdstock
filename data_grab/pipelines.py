# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class DataGrabPipeline:
    def process_item(self, item, spider):
        print(">>", item.get('company_name'))

        return item
