from .authentication import ApiManager
from labelme.models import User


class ApiCalls:

  @staticmethod
  def detect(apiManager, imageData):
    def call(oauthSession):
      url = apiManager.base_path + '/api/v1/detection/detect'
      files = {'media': imageData}
      response = oauthSession.post(url, files=files)
      print(response)

    apiManager.catchExpiredToken(call)

  @staticmethod
  def getProfile(apiManager):
    def call(oauthSession):
      url = apiManager.base_path + '/api/v1/users/profile'
      response = oauthSession.get(url)
      print(response)
      user = User.from_json(response.json())
      print(user)
      user.print_to_console()


    apiManager.catchExpiredToken(call)

    




