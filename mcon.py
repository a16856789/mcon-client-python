# -*- coding: utf-8 -*- 
import os
import sys
import json
import urllib
import urllib2

class ServiceProxy:
	serviceId = ''
	headers = {}
	def __init__(self, serviceId, headers = None):
		self.serviceId = serviceId
		self.headers = headers
	def invoke(self, methodName, args = []):
		url = "http://localhost:8124/proxy/invoke"
		data = urllib.urlencode({
			'headers': json.dumps(self.headers),
			'serviceId': self.serviceId,
			'methodName': methodName,
			'params': json.dumps(args)
		})
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
		request = urllib2.Request(url)
		response = opener.open(request, data) 
		json_result = response.read()
		result = json.loads(json_result)
		if result['success']:
			return result['response']
		else:
			raise Exception('' + result['error'])
	def method(self, methodName):
		def call(*args):
			return self.invoke(methodName, args)
		return call

def service(serviceId, headers = {}):
	return ServiceProxy(serviceId, headers)

if __name__ == '__main__':  
	echo_test = service('mcon.EchoTest');
	print echo_test.invoke('echo', ['hello invoke']);

	echo = echo_test.method('echo')
	print echo('hello, method')

	print echo(u'你好')

	echo_test.invoke('a', [])





