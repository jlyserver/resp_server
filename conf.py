#-*- coding: utf-8 -*-
import ConfigParser

class Picconf():
    def __init__(self, name):
        p = ConfigParser.ConfigParser()
        p.read(name)
        self.ip      = p.get('sys', 'ip')
        self.port    = p.getint('sys', 'port')

        self.dbserver_ip = p.get('db', 'dbserver_ip')
        self.dbserver_port=p.get('db', 'dbserver_port')

        self.msg     = p.get('ret', 'msg')
    def dis(self):
        print(self.port)

conf    = Picconf('./conf.txt')

if __name__ == "__main__":
    conf.dis()
