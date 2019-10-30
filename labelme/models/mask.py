id, :picture_id, :instance_number, :roi_x, :roi_y, :roi_x2, :roi_y2, :segmentation
class Mask:
  id = 0
  picture_id = 0
  instance_number = 0
  roi_x = 0
  roi_y = 0
  roi_x2 = 0
  roi_y2 = 0
  segmentation = []

  @staticmethod
  def from_json(json_obj):
    try:
      mask = Mask()
      mask.id = json_obj['id']
      mask.picture_id = json_obj['picture_id']
      mask.instance_number = json_obj['instance_number']
      mask.roi_x = json_obj['roi_x']
      mask.roi_y = json_obj['roi_y']
      mask.roi_x2 = json_obj['roi_x2']
      mask.roi_y2 = json_obj['roi_y2']
      mask.segmentation = json_obj['segmentation']
      
      return mask
    except:
      return None

  def print_to_console(self):
    print("Mask {")
    print("id: ", self.id)
    print("picture_id: ", self.picture_id)
    print("instance_number: ", self.instance_number)
    print("roi_x: ", self.roi_x)
    print("roi_y: ", self.roi_y)
    print("roi_x2: ", self.roi_x2)
    print("roi_y2: ", self.roi_y2)
    print("id: segmentation", self.segmentation)    
    print("}")

  def paint_to_canvas(self, canvas, color):  
    width = self.roi_x2 - self.roi_x
    height = self.roi_y2 - self.roi_y
    im = Image.new('RGBA', (width, height), color = (0,0,0,0))
    area = 0
    for x in range(width):
        for y in range(height):
            if self.segmentation[y][x] == "1":
                area += 1
                im.putpixel((x,y), color)
    qim = ImageQt(im)
    pix = QtGui.QPixmap.fromImage(qim)
    canvas.instances.append(pix)
    canvas.instances_bbox.append([self.roi_x,self.roi_y,self.roi_x2,self.roi_y2])
    canvas.instances_area.append(area)


  