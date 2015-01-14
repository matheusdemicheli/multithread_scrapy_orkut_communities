"""
Pipelines.
"""

import json
from scrapy_orkut_communities.utils import JsonFile


class JsonWriterPipeline(object):
    """
    Creates a fixture to be loaded in a django-model.
    """

    def process_item(self, item, spider):
        """
        Write in the file the content of item.
        """
        line = {}
        line['pk'] = None
        line['model'] = 'find.Community'
        line['fields'] = dict(item)
        line = json.dumps(line)

        if not hasattr(self, 'json_file'):
            self.json_file = JsonFile(spider=spider)
            self.json_file.file.write(line)
        else:
            self.json_file.file.write(',\n' + line)

        return item

    def close_spider(self, spider):
        """
        Close the file.
        """
        self.json_file.close_file()
