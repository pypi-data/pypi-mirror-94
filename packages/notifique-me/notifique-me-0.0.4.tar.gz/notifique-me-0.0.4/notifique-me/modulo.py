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
		self.connection = http.client.HTTPConnection('https://notifique-me.herokuapp.com')
		self.clienteId = clienteId
		self.secreteKey = secreteKey

		self.Authenticate()

	def __call__(self):
		print("call")

	def Authenticate(self):
		headers = {'Content-type': 'application/json'}
		self.connection.request('POST', '/api/login/autenticar/v1?clienteId='+str(self.clienteId)+'&secreteKey='+str(self.secreteKey), str(headers))
		response = self.connection.getresponse()
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
		self.connection.request('POST', '/api/Notificacao/v1', json_notification, headers)
		response = self.connection.getresponse()
		jsonRest = response.read().decode()
		return jsonRest

noti = Notification("929f5a28-a614-45aa-9889-2f0343046307", "K@CISK3-F#5UDK@D85#W57KC*IQINTQ058OTGO8#")
p = noti.Send(5531989715963, "5- Olá está é uma msg enviada pelo python", NotificationType.WHATSAPP)
print(p)