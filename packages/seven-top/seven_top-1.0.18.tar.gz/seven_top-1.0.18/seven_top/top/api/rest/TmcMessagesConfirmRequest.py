'''
Created by auto_sdk on 2018.10.23
'''
from seven_top.top.api.base import RestApi
class TmcMessagesConfirmRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.f_message_ids = None
		self.group_name = None
		self.s_message_ids = None

	def getapiname(self):
		return 'taobao.tmc.messages.confirm'
