import shutil
import scrapy
import datetime
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_base_url
from scrapy_orkut_communities import settings
from scrapy_orkut_communities.items import ScrapyOrkutCommunitiesItem
from scrapy_orkut_communities.utils import JsonFile


MAX_ITEMS = 10000


class OrkutCommunitiesSpider(scrapy.Spider):
    """
    Spider for get data from orkut communities.
    """
    name = "orkut_communities"
    handle_httpstatus_list = [404]

    def __init__(self, letter, global_file_name,
                 next_url, count, directory, *args, **kwargs):
        """
        Initiates the count_objects variable to keep control of the quantity
        of items processed.
        """
        self.letter = letter
        self.count_objects = 0

        self.globals = {
            'count': count,
            'next_url': next_url,
            'last_url': '',
            'error': '',
            'directory': directory
        }
        self.global_file_name = global_file_name

        self.start_urls = (next_url,)
        super(OrkutCommunitiesSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        Parse the pages witch contains the list of communities.
        """
        if response.status == 404:
            self.globals['last_url'] = self.globals['next_url']
            self.globals['next_url'] = self.globals['current_url']
            self.globals['error'] = 'Error 404 - %s' % response.url
            return

        self.globals['current_url'] = response.url

        items = response.css('.innerContainer .listCommunityContainer')
        items = items[1:-1]

        quantity_items = len(items) - 1
        quantity_total_items = quantity_items + self.count_objects

        for num, i in enumerate(items):
            self.count_objects += 1
            link = i.css('a').xpath('@href').extract()[0]
            link = urljoin_rfc(get_base_url(response), link)
            yield scrapy.Request(link, callback=self.parse_detail)

        next_page = response.xpath("//a[text()='next >']/@href").extract()
        if next_page:

            link = urljoin_rfc(get_base_url(response), next_page[0])

            if self.count_objects >= MAX_ITEMS:
                self.globals['last_url'] = self.globals['next_url']
                self.globals['next_url'] = link
                return

            yield scrapy.Request(link, callback=self.parse)

    def parse_detail(self, response):
        """
        Parse the detail of each community.
        """
        url = get_base_url(response)

        name = response.css('.commonHeader .archiveMessage')[0].xpath('text()')
        name = name.extract()[0]

        selector = '/html/body/div[2]/div/div[2]/div[1]/div[2]'
        description = ''.join(response.xpath(selector).css('div *').extract())

        image = response.css('.profilePicture').xpath('@src').extract()[0]
        url_image = 'http://orkut.google.com/%s' % image

        item = ScrapyOrkutCommunitiesItem(name=name,
                                          url=url,
                                          description=description,
                                          url_image=url_image)

        return item

    def closed(self, reason):
        """
        Saves globals.
        """
        data = '%s\n%s\n%s\n%s' % (
            self.globals['count'],
            self.globals['next_url'],
            self.globals['last_url'],
            self.globals['error']
        )

        global_file = open(self.global_file_name, 'w')
        global_file.write(data)
        global_file.close()
