'''
Created by auto_sdk on 2018.07.26
'''
from seven_top.top.api.base import RestApi
class TraderateImprImprwordsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cat_leaf_id = None
		self.cat_root_id = None

	def getapiname(self):
		return 'taobao.traderate.impr.imprwords.get'
