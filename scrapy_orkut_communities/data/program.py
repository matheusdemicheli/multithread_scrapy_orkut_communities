"""
Done for avoid memory leaks.
http://doc.scrapy.org/en/latest/topics/leaks.html

After some communities were collected, scrapy's process finishes and another
process is called. It still this until all communities were collected.

For each iteration, one new file is created to store the communities collected.


File: globals.txt

To keep control of the url to start each process, the information of the next
url to be visited is saved in the file "globals.txt", which works like a DB.
This file also includes information about the quantity of iterations, the letter
of the community had been and the last_url visited.
"""

import os
from subprocess import call
from threading import Thread

base_url = 'http://orkut.google.com/'

start_urls = {
    '#': '%sl-0.html' % base_url,
    'a': '%sl-a.html' % base_url,
    'b': '%sl-b.html' % base_url,
    'c': '%sl-c.html' % base_url,
    'd': '%sl-d.html' % base_url,
    'e': '%sl-e.html' % base_url,
    'f': '%sl-f.html' % base_url,
    'g': '%sl-g.html' % base_url,
    'h': '%sl-h.html' % base_url,
    'i': '%sl-i.html' % base_url,
    'j': '%sl-j.html' % base_url,
    'k': '%sl-k.html' % base_url,
    'l': '%sl-l.html' % base_url,
    'm': '%sl-m.html' % base_url,
    'n': '%sl-n.html' % base_url,
    'o': '%sl-o.html' % base_url,
    'p': '%sl-p.html' % base_url,
    'q': '%sl-q.html' % base_url,
    'r': '%sl-r.html' % base_url,
    's': '%sl-s.html' % base_url,
    't': '%sl-t.html' % base_url,
    'u': '%sl-u.html' % base_url,
    'v': '%sl-v.html' % base_url,
    'x': '%sl-x.html' % base_url,
    'y': '%sl-y.html' % base_url,
    'w': '%sl-w.html' % base_url,
    'z': '%sl-z.html' % base_url
}


class StartProcess(Thread):
    """
    Thread class for process simluntanious letters in orkut.com.
    """

    def __init__(self, letter, *args, **kwargs):
        """
        Save the current letter and url.
        """
        self.letter = letter
        self.start_url = start_urls[letter]

        self.directory = 'communities-%s' % self.letter

        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

        self.global_file_name = '%s/globals-%s.txt' % (
            self.directory,
            self.letter
        )

        if not os.path.exists(self.global_file_name):
            self._init_globals()

        super(StartProcess, self).__init__(*args, **kwargs)

    def _init_globals(self):
        """
        Inicializes the globals file.
        """
        count = 0
        next_url = self.start_url
        last_url = ''
        error = ''

        global_file = open(self.global_file_name, 'w')
        global_file.write('%s\n%s\n%s\n%s' % (count, next_url, last_url, error))
        global_file.close()

    def _get_globals(self):
        """
        Look at globals file and return the information.
        """
        global_file = open(self.global_file_name, 'r')
        count, next_url, last_url, error = global_file.read().split('\n')
        global_file.close()
        return count, next_url, last_url, error

    def run(self):
        """
        Runs the spider.
        """
        count, next_url, last_url, error = self._get_globals()

        while next_url != last_url and not error:

            call([
                "scrapy", "crawl", "orkut_communities",
                "-a",
                "letter=%s" % self.letter,
                "-a",
                "global_file_name=%s" % self.global_file_name,
                "-a",
                "next_url=%s" % next_url,
                "-a",
                "count=%s" % count,
                "-a",
                "directory=%s" % self.directory,
            ])
            count, next_url, last_url, error = self._get_globals()


if __name__ == "__main__":

    threads = []

    for letter in start_urls:
        threads.append(StartProcess(letter=letter))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
