#!/usr/bin/env python

import os.path
import os
from pstats import Stats

try:
    from urllib.parse import unquote_plus
except ImportError:
    from urllib import unquote_plus

import tornado.ioloop
import tornado.web

from stats import table_rows, json_stats
from profile import group_by_filenames


settings = {
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'debug': True,
    'gzip': True,
    'profile_dir': 'profile_dir'
}


class VizHandler(tornado.web.RequestHandler):
    def get(self, profile_name):
        normpath = os.path.normpath(profile_name)
        dirname = os.path.dirname(normpath)
        if dirname != self.application.settings['profile_dir']:
            raise tornado.web.HTTPError(404)

        profile_name = unquote_plus(profile_name)
        s = Stats(profile_name)
        self.render(
            'viz.html', profile_name=profile_name,
            table_rows=table_rows(s), callees=json_stats(s))


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        limit = int(self.get_argument('limit', 50))
        filenames = []
        for root, dirs, files in os.walk(self.application.settings['profile_dir']):
            for filename in files:
                filenames.append(os.path.join(root, filename))

        profile_group = group_by_filenames(filenames, limit=limit)
        self.render('index.html', profile_group=profile_group)


handlers = [(r'/snakeviz/(.*)', VizHandler),
            (r'/', IndexHandler)]

app = tornado.web.Application(handlers, **settings)

if __name__ == '__main__':
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
