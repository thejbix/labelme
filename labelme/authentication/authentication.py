import requests
import yaml
import __main__
import os

from qtpy import QtWidgets
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient

secrets_path = "labelme/config/secrets.yaml"

def open_secrets(secrets_path):
  with open(secrets_path, 'r') as stream:
    try:
        secrets = yaml.safe_load(stream)
        return secrets
    except yaml.YAMLError as exc:
        print(exc)
        return None

class Authentication:
  base_path = None
  client_id = None
  client_secret = None
  client_secret = None
  authorize_uri = None
  token_uri = None
  username = None
  password = None
  scope = 'user'
  access_token = None
  refresh_token = None

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
    authentication = Authentication()
    authentication.auth("jaydonbixenman@hotmail.com", "password")
    if authentication.signed_in():
      __main__.authentication = authentication
      self.accept()
    else:
      QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password')
  
  