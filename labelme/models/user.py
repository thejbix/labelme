
class User:
  id = 0
  first_name = None
  last_name = None
  email = None

  @staticmethod
  def from_json(json_obj):
    try:
      user = User()
      user.id = json_obj['id']
      user.first_name = json_obj['first_name']
      user.last_name = json_obj['last_name']
      user.email = json_obj['email']
      return user
    except:
      return None

  def print_to_console(self):
    print("User {")
    print("id: ", self.id)
    print("first_name: ", self.first_name)
    print("last_name: ", self.last_name)
    print("email: ", self.email)
    print("}")


  