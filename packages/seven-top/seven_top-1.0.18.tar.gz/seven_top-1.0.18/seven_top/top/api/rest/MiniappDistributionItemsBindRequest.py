'''
Created by auto_sdk on 2020.06.08
'''
from seven_top.top.api.base import RestApi
class MiniappDistributionItemsBindRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.add_bind = None
		self.target_entity_list = None
		self.url = None

	def getapiname(self):
		return 'taobao.miniapp.distribution.items.bind'
