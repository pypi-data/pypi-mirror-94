'''
Created by auto_sdk on 2018.07.25
'''
from seven_top.top.api.base import RestApi
class SellercenterRoleInfoGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.role_id = None

	def getapiname(self):
		return 'taobao.sellercenter.role.info.get'
