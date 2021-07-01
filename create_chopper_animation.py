#
# Generate an animated gif
#

import sys
from PIL import Image, ImageSequence, ImagePalette

def chopper_from_right_up():
    palette = [255, 255, 255, 0, 0, 0]
    new_frames = []

    chopper = Image.open("chopper.png")
    w,h = chopper.size

    for x in range(w,-w,-1):
        new_frame = Image.new(chopper.mode,chopper.size)
        new_frame.putpalette(palette)
        new_frame.paste(chopper,(x,0))
        new_frames.append(new_frame)
    return new_frames

def chopper_from_left_up():
    palette = [255, 255, 255, 0, 0, 0]
    new_frames = []

    chopper = Image.open("chopper.png")
    chopper = chopper.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = chopper.size

    for x in range(-w,w,1):
        new_frame = Image.new(chopper.mode,chopper.size)
        new_frame.putpalette(palette)
        new_frame.paste(chopper,(x,0))
        new_frames.append(new_frame)
    return new_frames

def chopper_from_right_down():
    palette = [255, 255, 255, 0, 0, 0]
    new_frames = []

    chopper = Image.open("chopper.png")
    w,h = chopper.size

    for x in range(w,-w,-1):
        new_frame = Image.new(chopper.mode,chopper.size)
        new_frame.putpalette(palette)
        new_frame.paste(chopper,(x,8))
        new_frames.append(new_frame)
    return new_frames

def chopper_from_left_down():
    palette = [255, 255, 255, 0, 0, 0]
    new_frames = []

    chopper = Image.open("chopper.png")
    chopper = chopper.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = chopper.size

    for x in range(-w,w,1):
        new_frame = Image.new(chopper.mode,chopper.size)
        new_frame.putpalette(palette)
        new_frame.paste(chopper,(x,8))
        new_frames.append(new_frame)
    return new_frames

def chopper_from_right_diagonally():
    palette = [255, 255, 255, 0, 0, 0]
    new_frames = []

    chopper = Image.open("chopper.png")
    w,h = chopper.size

    y = h
    for x in range(w,-w,-1):
        new_frame = Image.new(chopper.mode,chopper.size)
        new_frame.putpalette(palette)
        new_frame.paste(chopper,(x,int(y)))
        new_frames.append(new_frame)
        y -= float(2.0*h)/(2.0*w)
    return new_frames

def chopper_from_left_diagonally():
    palette = [255, 255, 255, 0, 0, 0]
    new_frames = []

    chopper = Image.open("chopper.png")
    chopper = chopper.transpose(Image.FLIP_LEFT_RIGHT)
    w,h = chopper.size

    y = h
    for x in range(-w,w,1):
        new_frame = Image.new(chopper.mode,chopper.size)
        new_frame.putpalette(palette)
        new_frame.paste(chopper,(x,int(y)))
        new_frames.append(new_frame)
        y -= float(2.0*h)/(2.0*w)
    return new_frames

def airwolf_from_right():
    palette = [255, 255, 255, 0, 0, 0]
    new_frames = []

    airwolf = Image.open("airwolf.png")
    w,h = airwolf.size
    new_w = 20

    for x in range(new_w,-w,-1):
        new_frame = Image.new(airwolf.mode,(new_w,15))
        new_frame.putpalette(palette)
        new_frame.paste(airwolf,(x,0))
        new_frames.append(new_frame)
    return new_frames


frames = []

chopper_frames = chopper_from_left_up()
frames += chopper_frames
chopper_frames = chopper_from_right_down()
frames += chopper_frames
chopper_frames = chopper_from_left_diagonally()
frames += chopper_frames
chopper_frames = chopper_from_right_up()
frames += chopper_frames
chopper_frames = chopper_from_left_down()
frames += chopper_frames
chopper_frames = chopper_from_right_diagonally()
frames += chopper_frames
airwolf_frames = airwolf_from_right()
frames += airwolf_frames
chopper_frames = chopper_from_left_diagonally()
frames += chopper_frames

print ("anim len= %s" % (len(frames)))
while len(frames) < 101*4:
    # Add empty frames
    frames.append(frames[0])

print "len: %s" % (len(frames))

im = frames[0]
im.save("chopper_anim_generated.gif",save_all=True, background=0, append_images=frames)

