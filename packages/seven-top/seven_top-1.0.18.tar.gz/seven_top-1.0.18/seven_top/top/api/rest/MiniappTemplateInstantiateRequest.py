'''
Created by auto_sdk on 2020.05.14
'''
from seven_top.top.api.base import RestApi
class MiniappTemplateInstantiateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.clients = None
		self.description = None
		self.ext_json = None
		self.icon = None
		self.name = None
		self.alias = None
		self.template_id = None
		self.template_version = None

	def getapiname(self):
		return 'taobao.miniapp.template.instantiate'
