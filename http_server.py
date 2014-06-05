#!/usr/bin/python
# coding: UTF-8

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from autopy import key, mouse
import urllib

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.splitquery(self.path)
        action = query[0]
        queryParams = {}

        if '?' in self.path:
            if query[1]:#接收get参数
                for qp in query[1].split('&'):
                    kv = qp.split('=')
                    queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8", 'ignore')

        content_type = "text/plain"
        content_type,content = {
            '/':index(queryParams,content_type),
            '/doublemove':doublemove(queryParams,content_type),
            '/singlemove':singlemove(queryParams,content_type),
            }.get(action,(content_type,"ERROR ACTION"))

        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content)
# end MyRequestHandler
 
# 打开主页
def index(queryParams,content_type):
    f = open('index.html')
    content = f.read()
    f.close()
    content_type = "text/html"
    return content_type,content

MOVE_LEFT  = 0
MOVE_RIGHT = 1
MOVE_UP    = 2
MOVE_DOWN  = 3
# 双指滑动
def doublemove(queryParams,content_type):
    content = "OK"
    if queryParams.has_key('direction') and queryParams.has_key('distance'):
        direction = int(queryParams['direction'])
        distance = int(queryParams['distance'])
        n = int(distance/50)
        print(direction,distance)
        if direction==MOVE_LEFT:
            for i in range(n):
                key.tap(key.K_LEFT)
        elif direction==MOVE_RIGHT:
            for i in range(n):
                key.tap(key.K_RIGHT)
        elif direction==MOVE_UP:
            for i in range(n):
                key.tap(key.K_UP)
        elif direction==MOVE_DOWN:
            for i in range(n):
                key.tap(key.K_DOWN)
        else:
            content = "no direction"
    return content_type,content

# 单指滑动
def singlemove(queryParams,content_type):
    content = "OK"
    if queryParams.has_key('disx') and queryParams.has_key('disy'):
        disx = int(queryParams['disx'])
        disy = int(queryParams['disy'])
        x,y = mouse.get_pos()
        xx,yy = disx+x,disy+y
        print(disx,disy,x,y,xx,yy)
        try:
            mouse.move(xx,yy)
        except ValueError:
            print("out of side")
    return content_type,content


if __name__=='__main__':
    try:
        httpd = HTTPServer(('', 8080), MyRequestHandler)
        print 'started httpserver...'
        httpd.serve_forever()

    except KeyboardInterrupt:
        httpd.socket.close()
    
    pass

