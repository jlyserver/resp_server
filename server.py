#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import hashlib
import os.path
import json
import time
import datetime
import re
import random

from tornado.options import define, options
from conf import conf

from xmlparse import order_response_xml_parse

define("port", default=conf.port, help="run on the given port", type=int)

class PayHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        xml = self.request.body
        d = order_response_xml_parse(xml)
        if d.get('return_code') == 'SUCCESS':
            print(d)
            openid = d['openid']
            otd    = d['out_trade_no']
            tid    = d['transaction_id']
            fee    = d['total_fee']
            headers = {'Content-Type':'text/html'}
            body = 'openid=%s&out_trade_no=%s&transaction_id=%&total_fee=%s'% (openid, otd, tid, fee)
            url = 'http://%s:%s/confirm_order' % (conf.dbserver_ip, conf.dbserver_port)
            http_client = tornado.httpclient.AsyncHTTPClient()
            resp = tornado.gen.Task(
                        http_client.fetch,
                        url, 
                        method='POST',
                        headers=headers,
                        body=body,
                        validate_cert=False)
            self.write(conf.msg)
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "xsrf_cookies": False,
        "debug":True}
    handler = [
               (r'/pay', PayHandler),
              ]
    application = tornado.web.Application(handler, **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
