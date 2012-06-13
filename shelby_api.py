import cherrypy
import json
import urllib
import httplib


client_id = "4fd8e4fc503dd407a4000086"
secret = "446cae12d4ea6a23c7d1c17840bcde4ac8e7662a05f712246368a3078747fcac"
redirect_url = "http://localhost:8080/bye"

class ShelbyApi(object):

  def __init__(self):
    self.token = None

  @cherrypy.expose
  def hello(self):
    uri = "http://localhost:3000/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&scope=" %(client_id, redirect_url)
    raise cherrypy.HTTPRedirect(uri)

  @cherrypy.expose
  def bye(self, code = "", **params):
    post_params = urllib.urlencode({"code": code, "client_id":client_id, "client_secret":secret, "grant_type":"authorization_code", "redirect_uri":redirect_url})
    conn = httplib.HTTPConnection("localhost:3000")
    conn.request("POST", "/oauth/access_token", post_params)
    response = conn.getresponse().read()
    self.token = json.loads(response)["access_token"]
    return """
    <a href="show"> Go Here </a>
    """
    
    

  @cherrypy.expose
  def show(self):
    return """<html>
    <body>
      <form name="input" action="hitapi" method="get">
        Url: <input type="text" name="url" />
        <input type="submit" value="Submit" />
      </form>
    </body>
    </html>"""

  
  @cherrypy.expose
  def hitapi(self, url = "", **params):
    if self.token is None:
      raise cherrypy.HTTPRedirect("hello")
    conn = httplib.HTTPConnection("localhost:3000")
    conn.request("GET", "/%s" %(url), headers = {"Authorization": "OAuth %s" %(self.token)})
    response = conn.getresponse().read()
    return response

cherrypy.quickstart(ShelbyApi())
    
