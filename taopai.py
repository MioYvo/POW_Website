#-*- coding: utf-8 -*-
import os
import paramiko
import Queue
import threading
import time

def starthadoop(queue):
	print "call starthadoop"
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('10.10.102.215',22,username='seclab',password='seclab',timeout=4)
	stdin,stdout,stderr = client.exec_command("cd /home/seclab/hadoop-2.2.0/;\
		./bin/hadoop jar /home/seclab/TT.jar /input/MR/in/veh /out")
		#hadoopsta = Queue.Queue()
	"""
	./bin/hadoop fs -rmr /out;
	./bin/hadoop fs -rmr /user/seclab/tmp*
	"""
	queue.put_nowait(stdout)
	return queue

def test(queue):
	if threading.activeCount():
		t1 = threading.Thread(taget=return_wait, args=())
		t2 = threading.Thread(taget=test_search, args=(queue))
		#status = "hadoop is done"
		#time.sleep(30)
		#queue.put_nowait(status)
		t1.start()
		t2.start()
		return queue
	else:
		return queue

def return_wait():
	return "wait ..."

def test_search(queue):
	print "-------------------call test_search------------------------"
	time.sleep(10)
	status = "hadoop is done"
	queue.put_nowait(status)

def test_result():
	print "-------------------call test_result------------------------"
	return "get part-00000 !!"


#cd /home/seclab/hadoop-2.2.0/
#./bin/hadoop fs -cat /out/part-00000

def search():
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('10.10.102.215', 22, username='seclab', password='seclab', timeout=4)
	stdin,stdout,stderr = client.exec_command("cd /home/seclab/hadoop-2.2.0/; \
		./bin/hadoop fs -cat /out/part-00000;\
        ")
	s = []
	for std in  stdout.readlines():
		s.append(std)
	print s[-1]
	client.close()
	return s

def ifexit():
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect('10.10.102.215', 22, username='seclab', password='seclab', timeout=4)
	stdin,stdout,stderr = client.exec_command("cd /home/seclab/hadoop-2.2.0/; \
		./bin/hadoop fs -ls /out;\
		")
	s = []
	for std in stdout.readlines():
		s.append(std)
	return len(s)