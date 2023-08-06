# -*- coding: utf-8 -*-
from __future__ import print_function
import http.client
import json

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace
class NotificationType:
	WHATSAPP = 0
	SMS = 1
	WHATSAPP_SMS = 2

class Notification:
	token = ""
	def __init__(self, clienteId, secreteKey):
		self.connection = http.client.HTTPSConnection('notifique-me.herokuapp.com')
		self.clienteId = clienteId
		self.secreteKey = secreteKey

		self.Authenticate()

	def __call__(self):
		print("call")

	def Authenticate(self):
		headers = {'Content-type': 'application/json'}
		self.connection.request('POST', '/api/Login/autenticar/v1?clienteId='+str(self.clienteId)+'&secreteKey='+str(self.secreteKey), str(headers))
		response = self.connection.getresponse()
		if (response.status == 401):
			return "Não autorizado, verifique suas credenciais."
		data = response.read().decode()
		obj = json.loads(data, object_hook=lambda d: Namespace(**d))
		Notification.token = obj.token
	
	def Send(self, number, msg, notificationType):
		headers = {
			'Authorization': 'Bearer '+str(Notification.token),
			'Content-Type': 'application/json'
		}

		body = {
			'Msg': msg,
			'Numero': number,
			'ClienteId': self.clienteId,
			"Type": notificationType
		}
		json_notification = json.dumps(body)
		print(json_notification)
		self.connection.request('POST', '/api/Notificacao/v1', json_notification, headers)
		response = self.connection.getresponse()
		if (response.status == 401):
			return "Não autorizado, verifique suas credenciais."
		jsonRest = response.read().decode()
		return jsonRest