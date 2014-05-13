#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'mio'

import threading
import Queue

import web
import MySQLdb
import dataprocess
import sendmail
import hp
import taopai
#import pyodbc
#import time



render = web.template.render('templates/')
#session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})  
#render=web.template.render('templates/',globals={"session":session})
urls = (
    #    '/','t1',
    '/dashborad', 'dashborad',
    #'/search', 'search',
    #'/search1', 'search1',
    '/heat', 'heat',
    '/','cover',
    '/signin','signin',
    '/login_ok', 'login_ok',
    '/login_error', 'login_error',
    '/logout','logout',
    '/early_warning','early_warning',
    '/hadoop','hadoop',
    '/hadoop_search','hadoop_search',
    #'/logout','cover'
)

app = web.application(urls, globals())

session = web.session.Session(app, web.session.DiskStore('sessions'),\
    initializer={'login':'', 'user':''})
#web.header('Content-disposition', 'attachment; filename=cover.html')
w = app.wsgifunc()

#web.sendmail('cookbook@webpy.org', 'user@example.com', 'subject', 'message')


class dashborad:
    def GET(self):
        if session.login == 1:
            row = dataprocess.POWprint("localtime","POWDATA")
            return render.dashborad(session.user,row)
        else:
            #raise web.seeother('/signin')
            return render.signin()
    def POST(self):
        if session.login == 1:
            data_search = web.input()
            #dataprocess.test1(data_search)
            prow = dataprocess.search(data_search)
            #type(data_search)
            #get data of form by 'name' property
            return render.search(session.user,prow)
        else :
            #raise web.seeother('/signin')
            return render.signin()

class cover(object):
    """docstring for cover"""
    def GET(self):
        return render.cover()

class signin(object):
    """docstring for signin"""
    def GET(self):
        #cookies = web.cookies(username="")
        #print cookies["username"]
        if session.login==1:
            raise web.seeother('/early_warning')
        else:
            return render.signin()

    def POST(self):
        user,passwd = web.input().user, web.input().passwd
        ident = dataprocess.checkin(user)
        try:
            if passwd == ident[0][1]:
                session.login=1
                session.user = user
                return render.login_ok(session.user)
            else :
                session.login=0
                return render.login_error(user)
        except:
            session.login=0
            return render.login_error(user)
        #print "user:", user, "password:", passwd
        
class login_ok:
    def GET(self):
        return render.login_ok()

class login_error:
    def GET(self):
        return render.login_error()

        
class logout:
    def GET(self):
        session.login=0
        session.kill()
        return render.logout()

class heat(object):
    def GET(self):
        if session.login == 1:
            pngdir = dataprocess.chartsprint()
            n = pngdir.keys()
            txtdir = dataprocess.heattxt()
            #print n
            #up = dataprocess.s_url(n)
            #cname = dataprocess.chartname()
            #dirname = dataprocess.POWprint("alltabname","POWDANA")
            #row = 
            return render.heat(session.user,pngdir,n,txtdir)
        else:
            return render.signin()
    def POST(self):
        if session.login == 1:
            data_search = web.input()
            prow = dataprocess.search(data_search)
            return render.search(session.user,prow)
        else:
            return render.signin()

class early_warning(object):
    """early_warning for POW"""
    def GET(self):
        if session.login == 1:
            pngdir = dataprocess.ew_chartsprint()
            n = pngdir.keys()
            txtdir = dataprocess.ew_txt()
            return render.early_warning(session.user,pngdir,n,txtdir)
            #return render.early_warning()
        else:
            return render.signin()
    def POST(self):
        if session.login == 1:
            data_search = web.input()
            prow = dataprocess.search(data_search)
            return render.search(session.user,prow)
        else:
            return render.signin()
        
class hadoop(object):
    """test hadoop site"""
    def GET(self):
        if session.login == 1:
            return render.hadoop(session.user)
        else:
            return render.signin()
    """
    def POST(self):
        data_search = web.input().search
        print data_search
        return render.hadoop_search(session.user,data_search)
    """

class hadoop_search(object):
    """function 1 : hadoop search"""
    """
    def GET(self):
        if session.login == 1:
            return render.hadoop_search(session.user," ")
        else:
            return render.signin()
    """
    def POST(self):
        if session.login == 1:
            data_search = web.input().search
            #print data_search
            print data_search
            result = hp.process(data_search)
            print result
            #return render.hadoop_search(session.user,prow)
            return render.hadoop_search(session.user,result)
        else:
            return render.signin()
        
        


if __name__ == "__main__":
#    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
#    app=fcgi.WSGIServer(index.appli,bindAddress=('0.0.0.0',9002),minSqare=0,maxSqare=8,maxChildren=8)
    app.run()
    sendmail.sendmail()
