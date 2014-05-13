#-*- coding: utf-8 -*-
import MySQLdb
import web
import dataprocess
import time

def sendmail():
	conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="liurusi321",charset="utf8")
	cursor = conn.cursor()
	cursor.execute("USE POWDATA;")
	cursor.execute("SELECT user FROM users;")
	u_names = cursor.fetchall()
	
	send_to = []
	for u in u_names:
		send_to.append(u[0])
	print send_to

	web.config.smtp_server = 'smtp.163.com'
	web.config.smtp_port = 25
	web.config.smtp_username = '13087550279@163.com'
	web.config.smtp_password = 'liu159762480*/-+'
	web.config.smtp_starttls = True

	send_from = '13087550279@163.com'

	ew = dataprocess.ew_chartsprint()
	#print len(ew.keys())
	urls = []
	for e in ew.keys():
		#print e
		urls.append("http:\\\localhost/heat#"+e)
	#web.sendmail(send_from, send_to, subject, body)
	#print urls
	body = "目前热点:"
	for u in urls:
		body = body+'   '+u.encode('utf8')
	#print body

	subject = 'POW热点预警'

	web.sendmail(send_from,'595766368@qq.com',subject,body)
#sendmail()