import contextlib
import random
import turtle
import time
from numpy import clip
from PIL import Image, ImageChops, ImageGrab, ImageMath

screen = turtle.Screen()
t = turtle.Turtle()
t.speed(0)
image = Image.open("turt.jpg")
image.thumbnail((1500,1000))
image = image.convert('RGB')
width, height = image.size
screen.setup(width, height)
t.ht()
failcount = 0
smallerim = Image.open("turt.jpg")
smallerim.thumbnail((50, 50))
colors = smallerim.getcolors(2500)
newcolors = []
for color in colors:
  newcolors.append(color[1][:3])
del colors, smallerim
current = ImageGrab.grab()
screencenter = current.size[0]//2, current.size[1]//2
windowshape = (width//-2+screencenter[0], height//-2+screencenter[1], width//2+screencenter[0], height//2+screencenter[1])
t.undobufferentries = 4

#---------------------------------------------------------------------
def finddiff(im1, im2):
  im1.thumbnail((200,200))
  im2.thumbnail((200,200))
  differntnes = 0
  diff = ImageChops.difference(im1, im2.convert('RGB'))
  colors = diff.getcolors(30000)

  for color in colors[:len(colors)//2]:
    differntnes += color[0] * (color[1][0] + color[1][1] + color[1][2])
  for color in colors[len(colors)//2:]:
    differntnes += color[0] * (color[1][0] + color[1][1] + color[1][2])
  return differntnes

#---------------------------------------------------------------------
def findrandshape(width, height):
  fixedwidth = width // 2
  fixedheight = height // 2
  fill = random.randrange(0, 2, 1)
  segments = random.randrange(1, 12, 1)
  degrees = random.randrange(0, 360, 1)
  locationx = random.randrange(-fixedwidth, fixedwidth, 1)
  locationy = random.randrange(-fixedheight, fixedheight, 1)
  rotation = random.randrange(0, 360, 1)
  size = random.randrange(0, 100, 4)
  red, green, blue = random.choice(newcolors)
  return [
      fill, segments, degrees, locationx, locationy, rotation, size, red,
      green, blue
  ]


#---------------------------------------------------------------------
def drawshape(shape):
  screen.colormode(255)
  t.pencolor((int(shape[7]), int(shape[8]), int(shape[9])))
  t.fillcolor((int(shape[7]), int(shape[8]), int(shape[9])))
  t.penup()
  t.setpos(int(shape[3]), int(shape[4]))
  t.pendown()
  t.setheading(int(shape[5]))
  t.begin_fill()
  with contextlib.suppress(ZeroDivisionError):
    t.circle(int(shape[6]), int(shape[2]), int(shape[1]))
  t.end_fill()


#---------------------------------------------------------------------

#creates a shape simmilar to "oldshape"
def adjust(old_shape, chaos):
  new_shape = old_shape[:]
  new_shape[1] = round(new_shape[1] + (random.random() * chaos))  #segments
  new_shape[2] = round(new_shape[2] + (random.random() * 5 * chaos))  #degrees
  new_shape[3] = round(new_shape[3] + (random.random() * 15 * chaos))  #location x
  new_shape[4] = round(new_shape[4] + (random.random() * 15 * chaos))  #location y
  new_shape[5] = round(new_shape[5] + (random.random() * 15 * chaos))  #roatation
  new_shape[6] = round(new_shape[6] + (random.random() * 15 * chaos))  #size
  new_shape[7] = round(new_shape[7] + (random.random() * 15 * chaos))  #red
  new_shape[8] = round(new_shape[8] + (random.random() * 15 * chaos))  #green
  new_shape[9] = round(new_shape[9] + (random.random() * 15 * chaos))  #blue

  new_shape[7:] = clip(new_shape[7:], 0, 255)

  return new_shape


#---------------------------------------------------------------------
input('Press Enter to Begin...')
while True:
  with open('shapes.txt','r') as f:
    shapes = f.read()
  shapes = shapes.split("\n")
  best = 1000000000
  bestcirc = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  screen.tracer(0, 0)

  #sets up the screen
  for j in range(len(shapes)-1):
    shape = shapes[j][1:-1].split(",")
    drawshape(shape)

  before = shapes[-2].replace('(', '').split(',')
  before = int(before[0])
  difference = 1000000000
  del shapes

  #accounts for an off by one error in the next loop
  t.forward(1)
  t.forward(1)
  t.forward(1)

  #----------------------------------------------
    
  #creates 50 random shapes and keeps the best
  for i in range(50):
    t.undo()
    t.undo()
    t.undo()

    circlestat = findrandshape(width, height)

    #draws the shape to measure it's helpfulness
    drawshape(circlestat)
    screen.update()
    current = ImageGrab.grab(bbox=windowshape)
    difference = finddiff(image, current)

    if best > difference:
      bestcirc = circlestat
      best = difference

  for i in range(25):   
    new = adjust(bestcirc, 5 /(1+i))
    t.undo()
    t.undo()
    t.undo()
    drawshape(new)
    screen.update()
    current = ImageGrab.grab(bbox=windowshape)
    difference = finddiff(image, current)
    if best > difference:
      bestcirc = new
      best = difference
  #----------------------------------------------
  if best < before:
    bestcirc[0] = best
    try:
      print("win")
      failcount = 0
      with open("shapes.txt", "a") as f:
        f.write(str(tuple(bestcirc))+"\n")
    except UnboundLocalError:
      pass
  else:
    print('fail')
    t.undo()
    t.undo()
    t.undo()
    failcount += 1
    print(failcount)
    #failcount is a way to ensure progress is being made, will reset when progress is made

  t.clear()
