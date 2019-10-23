import requests
import yaml
from qtpy import QtGui
import labelme.main

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient




config_path = "../config/"

client_id = 
client_secret = 'PJ6aLnVpAC77Ad7-Yg1coVCGm1zbNH1znk8MMWprm8Q'
redirect_uri = 'cowcounteroauth://connect/callback'
base = 'https://58a36bc0.ngrok.io'
authorization_uri = base + "/oauth/authorize"
token_uri = base + "/oauth/token"
scope = "user"

def open_secrets(config_path, file_name):
  file_path = config_path + file_name
  with open(file_path, 'r') as stream:
    try:
        secrets = yaml.safe_load(stream)
        return secrets
    except yaml.YAMLError as exc:
        print(exc)
        return None

class Authentication:
  self.base_path = None
  self.client_id = None
  self.client_secret = None
  self.client_secret = None
  self.authorize_uri = None
  self.token_uri = None
  self.username = None
  self.password = None
  self.scope = 'user'
  self.access_token = None
  self.refresh_token = None

  def __init__(self):
    secrets = open_secrets(config_path, "secrets.yaml")
    if secrets != None:
      api = secrets['CowCounterAPI']
      self.base_path = api['base_path']
      self.client_id = api['client_id']
      self.client_secret = api['client_secret']
      self.client_secret = api['client_secret']
      self.authorize_uri = api['authorize_uri']
      self.token_uri = api['token_uri']

  # return true on success
  def auth(self, username, password):
    self.username = username
    self.password = password
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id), scope=self.scope)
    try:
      token = oauth.fetch_token(
          token_url=self.base_path + self.token_uri, 
          username=self.username,
          password=self.password, 
          client_id=self.client_id, 
          client_secret=self.client_secret)
      self.access_token = token['access_token']
      self.refresh_token = token['refresh_token']
      return True
    except:
      return False
    
  # return true on success
  def refresh(self):
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id), scope=self.scope)
    try:
      token = oauth.refresh_token(
          token_url=self.base_path + self.token_uri, 
          refresh_token=self.refresh_token, 
          client_id=self.client_id, 
          client_secret=self.client_secret)
      self.access_token = token['access_token']
      self.refresh_token = token['refresh_token']
      return True
    except:
      return False

  def signed_in(self):
    if self.access_token != None:
      return True
    else:
      return False

class Login(QtGui.QDialog):

  def __init__(self, parent=None):
    super(Login, self).__init__(parent)
    self.txtUsername = QtGui.QLineEdit(self)
    self.txtPassword = QtGui.QLineEdit(self)
    self.btnLogin = QtGui.QPushButton('Login', self)
    self.btnLogin.clicked.connect(self.handleLogin)
    layout = QtGui.QVBoxLayout(self)
    layout.addWidget(self.txtUsername)
    layout.addWidget(self.txtPassword)
    layout.addWidget(self.btnLogin)

  def handleLogin(self):
    authentication = Authentication()
    authentication.auth("jbixenman@cropquest.com", "password")
    if authentication.signed_in():
      main.authentication = authentication
      self.accept()
     
    