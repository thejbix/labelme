from .authentication import ApiManager


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
      print(response.json())

    apiManager.catchExpiredToken(call)

    




