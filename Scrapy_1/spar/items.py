import scrapy


class SparItem(scrapy.Item):
    # define the fields for your item here like:

    _id = scrapy.Field()
    name_store = scrapy.Field()
    pictures = scrapy.Field()
    pictures_cat_name = scrapy.Field()
    pic_name = scrapy.Field()
    pictures_cat = scrapy.Field()
    main_category_name = scrapy.Field()
    category_img_url = scrapy.Field()
    category_img = scrapy.Field()
    main_category_img = scrapy.Field()
    category_name = scrapy.Field()
    category_permalink = scrapy.Field()
    product_name = scrapy.Field()
    product_img_link = scrapy.Field()
    product_instamart_price = scrapy.Field()
    product_original_unit_price = scrapy.Field()
    product_price = scrapy.Field()
    product_unit_price = scrapy.Field()
    product_discount = scrapy.Field()
    product_human_volume = scrapy.Field()
    product_items_per_pack = scrapy.Field()
    product_price_type = scrapy.Field()
    product_stock = scrapy.Field()
    product_description = scrapy.Field()
    product_description_original = scrapy.Field()
    product_properties = scrapy.Field()
    product_nutrition = scrapy.Field()