
class Picture:
  id = 0
  detection_ran = False

  @staticmethod
  def from_json(json_obj):
    try:
      picture = Picture()
      picture.id = json_obj['id']
      picture.detection_ran = json_obj['detection_ran']
      return picture
    except:
      return None

  def print_to_console(self):
    print("Picture {")
    print("id: ", self.id)
    print("detection_ran: ", self.detection_ran)
    print("}")


  