from google.appengine.ext import webapp
import jinja2
import os
import base64
import random
import math

jinja_environment=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')))


class MainHandler(webapp.RequestHandler):
	def get(self):
		template=jinja_environment.get_template('index.html')
		self.response.out.write(template.render())


app = webapp.WSGIApplication([('/', MainHandler)],
							 debug=True)

