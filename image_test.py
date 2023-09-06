from PIL import Image
import math

foo = Image.open("shot.png")
x, y = foo.size
x2, y2 = math.floor(x-50), math.floor(y-20)
foo = foo.resize((x2,y2),Image.ANTIALIAS)
foo.save("path\\to\\save\\image_scaled.jpg",quality=95)


x, y = foo.size
x2, y2 = math.floor(x-20), math.floor(y-50)