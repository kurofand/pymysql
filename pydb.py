# -*-coding:utf-8 -*-

import re
import mysql.connector

class Db:
	user=''
	password=''
	host=''
	dbName=''
	connected=False
	def __init__(self, fileName):
		ini=open(fileName, 'r')
		param=[]
		for str in ini:
			param.append(str[:-1])
		self.host=param[0]
		self.dbName=param[1]
		self.user=param[2]
		self.password=param[3]

	def connect(self):
		if(not self.connected):
			try:
				self.connection=mysql.connector.connect(host=self.host, database=self.dbName, user=self.user, password=self.password)
				self.connected=True
				return True
			except:
				print('Connection error!')
				return False

	def executeQuery(self, query):
		if(self.connected):
			cursor=self.connection.cursor(dictionary=True)
			if(re.search('(^SELECT)|(^select)', query)):
				cursor.execute(query)
				return cursor
			elif(re.search('(^INSERT)|(^insert)|(^ALTER)|(^alter)|(^DELETE)|(^delete)', query)):
				try:
					cursor.execute(query)
					self.connection.commit()
					return True
				except mysql.connector.Error as e:
					print('%s'%str(e))
					return False

	def closeConnection(self):
		if(self.connected):
			self.connection.close()
			self.connected=False
