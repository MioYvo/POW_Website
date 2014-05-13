#-*- coding: utf-8 -*-
import commands
import os

def process(operating):
	#result = list(commands.getstatusoutput("""%s"""%(operating)))
	#print result
	#return result[1].decode('utf-8')
	print operating

	result = os.popen("""
		python '/home/mio/Desktop/testANA/t13.py'
		""").readlines()
	return result
