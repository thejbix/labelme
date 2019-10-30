import requests
import yaml
import __main__
import os

from qtpy import QtWidgets
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2 import TokenExpiredError

secrets_path = "labelme/config/secrets.yaml"

def open_secrets(secrets_path):
  with open(secrets_path, 'r') as stream:
    try:
        secrets = yaml.safe_load(stream)
        return secrets
    except yaml.YAMLError as exc:
        print(exc)
        return None

class ApiManager:
  base_path = None
  client_id = None
  client_secret = None
  client_secret = None
  authorize_uri = None
  token_uri = None
  username = None
  password = None
  scope = 'user'
  token = None

  def __init__(self):
    global secrets_path
    secrets = open_secrets(secrets_path)
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
      print(token)
      self.token = token
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
      self.token = token
      return True
    except:
      return False

  def signed_in(self):
    if self.token != None:
      return True
    else:
      return False

  def catchExpiredToken(self, webcall):
    loopMax = 2
    for i in range(loopMax):
      print("catchExpiredToken ", i)
      if i == (loopMax - 1):
        try:
          oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id), scope=self.scope, token=self.token)
          response = webcall(oauth)
          return response
        except:
          return None
      else:
        try:
          oauth = OAuth2Session(client=LegacyApplicationClient(client_id=self.client_id), scope=self.scope, token=self.token)
          response = webcall(oauth)
          return response
        except:
          self.refresh()


  
class Login(QtWidgets.QDialog):

  def __init__(self, parent=None):
    super(Login, self).__init__(parent)
    self.txtUsername = QtWidgets.QLineEdit(self)
    self.txtPassword = QtWidgets.QLineEdit(self)
    self.btnLogin = QtWidgets.QPushButton('Login', self)
    self.btnLogin.clicked.connect(self.handleLogin)
    layout = QtWidgets.QVBoxLayout(self)
    layout.addWidget(self.txtUsername)
    layout.addWidget(self.txtPassword)
    layout.addWidget(self.btnLogin)

  def handleLogin(self):
    apiManager = ApiManager()
    apiManager.auth("jaydonbixenman@hotmail.com", "password")
    if apiManager.signed_in():
      __main__.apiManager = apiManager
      self.accept()
    else:
      QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password')
  
  