import scrapy
from scrapy.http import HtmlResponse
from spar.items import SparItem


class MysparruSpider(scrapy.Spider):
    name = 'mysparru'
    allowed_domains = ['myspar.ru']
    start_urls = ['https://myspar.ru/catalog/']
    method = 'POST'
    def parse(self, response: HtmlResponse):
        ra = {}
        ra['main_cat_name'] = response.xpath('//a[@class="section-tile__title js-title-links-open"]/span//text()').getall()
        ra['main_cat_link'] = response.xpath('//picture/source[@type="image/webp"]/@data-srcset').getall()
        links = response.xpath("//a[@class='section-tile__title js-title-links-open']/@href").getall()

        for link in links:
            yield response.follow(link, callback=self.category_up_parse, method='post', cb_kwargs=ra)


    def category_up_parse(self, response: HtmlResponse, **kwargs):
        ram = {}
        ram['cat_name'] = response.xpath('//a[@class="section-tile__title"]/span//text()').getall()
        ram['cat_link'] = response.xpath('//picture/source[@type="image/webp"]/@data-srcset').getall()
        kwargs.update(ram)
        links = response.xpath("//a[@class='section-tile__title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.category_parse, method='post', cb_kwargs=kwargs)



    def category_parse(self, response: HtmlResponse, **kwargs):

        next_page = response.xpath("//a[@class='paging__control paging__control--next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.category_parse, method='post', cb_kwargs=kwargs)

        products = response.xpath("//a[@class='catalog-tile__link js-analytic-click']/@href").getall()
        for product in products:
            yield response.follow(product, callback=self.product_parse, method='post', encoding='utf-8', cb_kwargs=kwargs)

    def product_parse(self, response: HtmlResponse, **kwargs):

        pic_name = kwargs['main_cat_name']
        pictures = kwargs['main_cat_link']

        pictures_cat = kwargs['cat_link']
        pictures_cat_name = kwargs['cat_name']
        name_stor = 'Спар'
        main_category_nam = response.xpath("//span[@itemprop='name']//text()").getall()
        product_nam = response.xpath("//div[@class='catalog-element__head']/h1//text()").get()
        product_img_lin = response.xpath("//picture//source/@data-srcset").get()
        product_instamart_pric = response.xpath("//span[@class='prices__old']//text()").get()
        product_original_unit_pric = response.xpath("//span[@class='prices__old']//text()").get()
        product_pric = response.xpath("//span[@class='prices__cur js-item-price']//text()").get()
        product_unit_pric = response.xpath("//span[@class='prices__cur js-item-price']//text()").get()
        product_discoun = response.xpath("//span[@class='discount']/span//text()").get()
        product_human_volum = response.xpath("//div[@class='catalog-element__avg']//text()").get()
        product_items_per_pack = None
        product_price_typ = response.xpath("//span[@class='js-unit prices__unit active']/@data-unit//text()").get()
        product_stoc = response.xpath("//div[@class='catalog-element__no-available']//text()").get()
        product_descriptio = response.xpath("//p[@itemprop='description']//text()").get()
        product_description_origina = response.xpath("//p[@itemprop='description']//text()").get()
        product_propertie = response.xpath("//div[@class='col-lg-6']//text()").getall()
        product_nutritio = response.xpath("//div[@class='row no-gutters']//text()").getall()

        yield SparItem(product_items_per_pack=product_items_per_pack, pictures_cat_name=pictures_cat_name,
                       pic_name=pic_name, pictures_cat=pictures_cat, pictures=pictures, name_store=name_stor,
                       main_category_name=main_category_nam, product_name=product_nam, product_img_link=product_img_lin,
                       product_instamart_price=product_instamart_pric,
                       product_original_unit_price=product_original_unit_pric, product_price=product_pric,
                       product_unit_price=product_unit_pric, product_discount=product_discoun,
                       product_human_volume=product_human_volum, product_price_type=product_price_typ,
                       product_stock=product_stoc, product_description=product_descriptio,
                       product_description_original=product_description_origina, product_properties=product_propertie,
                       product_nutrition=product_nutritio)