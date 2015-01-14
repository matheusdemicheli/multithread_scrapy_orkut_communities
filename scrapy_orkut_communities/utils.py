"""
Utils for the project.
"""

class JsonFile(object):
    """
    Controls the storage file.
    """

    def __init__(self, spider):
        """
        Open the file.
        """
        self.spider = spider
        self.open_file()

    def open_file(self):
        """
        Open a new file.
        """
        count = int(self.spider.globals['count']) + 1
        self.spider.globals['count'] = str(count)

        self.file_name = '%s/community-%s-%s.json' % (
            self.globals['directory'],
            self.spider.letter,
            self.spider.globals['count']
        )

        self.file = open(self.file_name, 'wb')
        self.file.write('[\n')

    def close_file(self):
        """
        Close the file.
        """
        self.file.write('\n]')
        self.file.close()
