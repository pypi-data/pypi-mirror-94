'''
Created by auto_sdk on 2020.03.28
'''
from seven_top.top.api.base import RestApi
class ItemcatsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cids = None
		self.datetime = None
		self.fields = None
		self.parent_cid = None

	def getapiname(self):
		return 'taobao.itemcats.get'
