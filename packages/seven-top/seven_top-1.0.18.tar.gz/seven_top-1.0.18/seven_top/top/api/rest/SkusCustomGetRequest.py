'''
Created by auto_sdk on 2019.10.31
'''
from seven_top.top.api.base import RestApi
class SkusCustomGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.outer_id = None

	def getapiname(self):
		return 'taobao.skus.custom.get'
