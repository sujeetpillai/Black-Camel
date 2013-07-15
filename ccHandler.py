from google.appengine.ext import webapp
from google.appengine.ext import db
import os
import base64
import random
import math
import json
import time
import datetime
import logging

class ccHandler(webapp.RequestHandler):
	def post(self):
		jstr=self.request.POST['trxStore'];
		logging.log(logging.INFO,jstr)
		trxStore=json.loads(jstr)
		for trx in trxStore:
			amt=float(trx['amount'].replace(',',''))
			dt=time.strftime('%m/%d/%Y',time.strptime(trx['date'],'%d %b %y'))
			trans=Transaction(merchant=trx['merchant'],amount=amt,card=trx['card'],date=dt)
			trans.put()

		totalBillable=0.0
		try:
			q=Transaction.all()
			today=datetime.date.today()
			if today.day>=13:
				current_billcycle_start = datetime.date(year=today.year,month=today.month,day=13)
			else:
				if today.month==1:
					month=12
					year=today.year-1
				else:
					month=today.month
					year=today.year
				current_billcycle_start = datetime.date(year=year,month=month,day=13)


			for t in q.run():
				if datetime.datetime.strptime(t.date,'%m/%d/%Y').date()>=current_billcycle_start:
					totalBillable=totalBillable+t.amount
		except Exception as exc:
			print exc

		self.response.write('OK|'+str(totalBillable))


class Transaction(db.Model):
	merchant=db.StringProperty(required=True)
	amount=db.FloatProperty(required=True)
	card=db.StringProperty(required=True)
	date=db.StringProperty(required=True)


app = webapp.WSGIApplication([('/ccHandler', ccHandler)],debug=True)
