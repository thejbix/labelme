from .authentication import ApiManager
from labelme.models import User


class ApiCalls:

  @staticmethod
  def detect(apiManager, imageData):
    def call(oauthSession):
      url = apiManager.base_path + '/api/v1/detection/detect'
      files = {'media': imageData}
      response = oauthSession.post(url, files=files)
      print(response.json())
      return response
    return apiManager.catchExpiredToken(call)

  @staticmethod
  def getProfile(apiManager):
    def call(oauthSession):
      url = apiManager.base_path + '/api/v1/users/profile'
      response = oauthSession.get(url)
      user = User.from_json(response.json())
      return user
    return apiManager.catchExpiredToken(call)

  @staticmethod
  def fetchResults(apiManger, picture):
    def call(oauthSession):
      url = apiManager.base_path + '/api/v1/detection/fetch_masks_from_picture'
      response = requests.get(url)
      json_response = response.json()
      masks = []
      for mask_json in json_response:
        mask = Mask.from_json(mask_json)
        masks.append(mask)
      return masks

    apiManager.catchExpiredToken(call)
    




