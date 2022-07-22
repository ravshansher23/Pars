import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class SparPipeline:





    def process_item(self, item, spider):

        item['main_category_name'], item['category_name'] = self.name_main(item['main_category_name'])
        item['product_price_type'] = self.price_type(item['product_price_type'])
        item['product_properties'] = self.properties(item['product_properties'])
        item['product_nutrition'] = self.product_nutrition(item['product_nutrition'])
        item['product_stock'] = self.product_on_stock(item['product_stock'])

        return item



    def name_main(self, main_category_name):
        try:
            main = main_category_name[2]
            category_name = main_category_name[3]
            return main, category_name
        except Exception as err:
            main = None
            category_name = None
            return main, category_name



    def product_nutrition(self, product_nutrition):
        items = [idx for idx in product_nutrition if idx[0] != "\n"]

        for i in items:
            if i == '':
                items.remove(i)

        i_dict = [{items[i]: items[i + 1] for i in range(0, len(items) - 1, 2)}]
        return i_dict

    def product_on_stock(self, product):
        if product:
            item = 'no stock'
            return item
        else:
            item = 'on stock'
            return item
    def price_type(self, product_price_type):
        if product_price_type == 'кг':
            item = 'per_kilo'
            return item
        else:
            item = 'per_pack'
            return item

    def properties(self, product_properties):

        items = [idx for idx in product_properties if idx[0] != "\n"]

        for i in items:
            if i == '':
                items.remove(i)

        i_dict = [{items[i]: items[i + 1] for i in range(1, len(items) - 1, 2)}]

        prop = {
            items[0]: i_dict
        }
        return prop




class SparPicPipeline:

    def process_item(self, item, spider):
        item['main_category_img'] = self.picture(item['pictures'], item['pic_name'], item['main_category_name'])
        item['category_img_url'] = self.picture(item['pictures_cat'], item['pictures_cat_name'], item['category_name'])
        return item



    def picture(self, links, names, category_name):
        pic_dict = {}
        if category_name:
            try:
                for i in range(len(names)):
                    pic_dict[names[i]] = links[i]
                    if category_name == names[i]:
                        category_name = names[i]

                result = pic_dict[category_name]
                return result
            except Exception as err:
                return None
        else:
            return None

class SparPicDownload(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['main_category_img']:
            res = item['main_category_img']
            try:
                yield scrapy.Request(res, method='GET')
            except Exception as err:
                print(err)

        if item['category_img_url']:
            rest = item['category_img_url']
            try:
                yield scrapy.Request(rest, method='GET')
            except Exception as err:
                print(err)

        if item['product_img_link']:
            rest = item['product_img_link']
            try:
                yield scrapy.Request(rest, method='GET')
            except Exception as err:
                print(err)

    def item_completed(self, results, item, info):
        if results:
            try:
                item['main_category_img'] = results[0]
            except Exception as err:
                print(err)
            try:
                item['category_img_url'] = results[1]
            except Exception as err:
                print(err)
            try:
                item['product_img_link'] = results[2]
            except Exception as err:
                print(err)
        return item

class SparPicPipelineTwo:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.spar1

    def process_item(self, item, spider):
        r = str(item['product_instamart_price'])
        item['product_instamart_price'] = r.strip('\xa0₽')
        w = str(item['product_original_unit_price'])
        item['product_original_unit_price'] = w.strip('\xa0₽')
        item['pictures_cat_name'] = None
        item['pic_name'] = None
        item['pictures_cat'] = None
        item['pictures'] = None
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item