#
# Generate an animated gif
#

import sys
from PIL import Image, ImageSequence, ImagePalette

def add_death():

    palette = [255, 255, 255, 0, 0, 0]

    gif = Image.open("img/animation_death.gif")

    pacman_dies = []
    for gif_frame in ImageSequence.Iterator(gif):
        gif_frame = gif_frame.convert('P')
        gif_frame.putpalette(palette)
        pacman_dies.append(gif_frame.copy().convert('P'))

    return pacman_dies
    

def add_pacman():

    palette = [255, 255, 255, 0, 0, 0]
    frames = []

    gif = Image.open("img/animation.gif")

    pacman_up_going_right = []
    #gif_frames = ImageSequence.Iterator(gif)
    for gif_frame in ImageSequence.Iterator(gif):
        gif_frame = gif_frame.convert('P')
        gif_frame.putpalette(palette)
        pacman_up_going_right.append(gif_frame.copy().convert('P'))
    frames.append(pacman_up_going_right)

    pacman_up_going_left = []
    for gif_frame in pacman_up_going_right:
        gif_frame = gif_frame.transpose(Image.FLIP_LEFT_RIGHT)
        pacman_up_going_left.append(gif_frame.copy())
    frames.append(pacman_up_going_left)

    pacman_down_going_right = []
    for gif_frame in pacman_up_going_right:
        new_frame = Image.new(gif_frame.mode, gif_frame.size)
        new_frame.putpalette(palette)
        new_frame.paste(gif_frame, (0, 8))
        pacman_down_going_right.append(new_frame)
    frames.append(pacman_down_going_right)

    pacman_down_going_left = []
    for gif_frame in pacman_up_going_left:
        new_frame = Image.new(gif_frame.mode, gif_frame.size)
        new_frame.putpalette(palette)
        new_frame.paste(gif_frame, (0, 8))
        pacman_down_going_left.append(new_frame)
    frames.append(pacman_down_going_left)

    pacman_both_up_going_left = []
    for i in range(0, len(pacman_down_going_right)):
        tmp = pacman_up_going_left[i]
        up = pacman_up_going_left[i].copy().crop((0,0,4*5,7))
        down = pacman_down_going_right[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        pacman_both_up_going_left.append(new_frame)
    frames.append(pacman_both_up_going_left)

    pacman_both_up_going_right = []
    for i in range(0, len(pacman_down_going_left)):
        tmp = pacman_up_going_right[i]
        up = pacman_up_going_right[i].copy().crop((0,0,4*5,7))
        down = pacman_down_going_left[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        pacman_both_up_going_right.append(new_frame)
    frames.append(pacman_both_up_going_right)

    pacman_both_going_right = []
    for i in range(0, len(pacman_down_going_right)):
        tmp = pacman_up_going_right[i]
        up = pacman_up_going_right[i].copy().crop((0,0,4*5,7))
        down = pacman_down_going_right[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        pacman_both_going_right.append(new_frame)
    frames.append(pacman_both_going_right)

    pacman_both_going_left = []
    for i in range(0, len(pacman_down_going_left)):
        tmp = pacman_up_going_left[i]
        up = pacman_up_going_left[i].copy().crop((0,0,4*5,7))
        down = pacman_down_going_left[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        pacman_both_going_left.append(new_frame)
    frames.append(pacman_both_going_left)

    return frames

def add_ghost():

    palette = [255, 255, 255, 0, 0, 0]
    frames = []

    gif = Image.open("img/animation_ghost.gif")

    # 0
    ghost_up_going_right = []
    #gif_frames = ImageSequence.Iterator(gif)
    for gif_frame in ImageSequence.Iterator(gif):
        gif_frame = gif_frame.convert('P')
        gif_frame.putpalette(palette)
        ghost_up_going_right.append(gif_frame.copy())
    frames.append(ghost_up_going_right)

    # 1
    ghost_up_going_left = []
    for gif_frame in ghost_up_going_right:
        gif_frame = gif_frame.transpose(Image.FLIP_LEFT_RIGHT)
        ghost_up_going_left.append(gif_frame.copy())
    frames.append(ghost_up_going_left)

    # 2
    ghost_down_going_right = []
    for gif_frame in ghost_up_going_right:
        new_frame = Image.new(gif_frame.mode, gif_frame.size)
        new_frame.putpalette(palette)
        new_frame.paste(gif_frame, (0, 8))
        ghost_down_going_right.append(new_frame)
    frames.append(ghost_down_going_right)

    # 3
    ghost_down_going_left = []
    for gif_frame in ghost_up_going_left:
        new_frame = Image.new(gif_frame.mode, gif_frame.size)
        new_frame.putpalette(palette)
        new_frame.paste(gif_frame, (0, 8))
        ghost_down_going_left.append(new_frame)
    frames.append(ghost_down_going_left)

    # 4
    ghost_both_up_going_left = []
    for i in range(0, len(ghost_down_going_right)):
        tmp = ghost_up_going_left[i]
        up = ghost_up_going_left[i].copy().crop((0,0,4*5,7))
        down = ghost_down_going_right[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        ghost_both_up_going_left.append(new_frame)
    frames.append(ghost_both_up_going_left)

    # 5
    ghost_both_up_going_right = []
    for i in range(0, len(ghost_down_going_left)):
        tmp = ghost_up_going_right[i]
        up = ghost_up_going_right[i].copy().crop((0,0,4*5,7))
        down = ghost_down_going_left[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        ghost_both_up_going_right.append(new_frame)
    frames.append(ghost_both_up_going_right)

    # 6
    ghost_both_going_right = []
    for i in range(0, len(ghost_down_going_right)):
        tmp = ghost_up_going_right[i]
        up = ghost_up_going_right[i].copy().crop((0,0,4*5,7))
        down = ghost_down_going_right[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        ghost_both_going_right.append(new_frame)
    frames.append(ghost_both_going_right)

    # 7
    ghost_both_going_left = []
    for i in range(0, len(ghost_down_going_left)):
        tmp = ghost_up_going_left[i]
        up = ghost_up_going_left[i].copy().crop((0,0,4*5,7))
        down = ghost_down_going_left[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        ghost_both_going_left.append(new_frame)
    frames.append(ghost_both_going_left)

    return frames

def merge_up_and_down(up_in, down_in):
    palette = [255, 255, 255, 0, 0, 0]
    frames = []
    for i in range(0, len(up_in)):
        tmp = up_in[0]
        up = up_in[i].copy().crop((0,0,4*5,7))
        down = down_in[i].copy().crop((0,8,4*5,15))
        new_frame = Image.new(tmp.mode, tmp.size)
        new_frame.putpalette(palette)
        new_frame.paste(up, (0,0))
        new_frame.paste(down, (0, 8))
        frames.append(new_frame)
    return frames

frames = []

pacman_frames = add_pacman()
ghost_frames = add_ghost()
pacman_right_ghost_left_frame = merge_up_and_down(pacman_frames[0], ghost_frames[3])
pacman_left_ghost_right_frame = merge_up_and_down(ghost_frames[1], pacman_frames[2])
death_frames = add_death()

# Running order
# pacman ->
frames += pacman_frames[0]
# ghost <-
frames += ghost_frames[3]
# pacman <-
frames += pacman_frames[3]
# ghost ->
frames += ghost_frames[0]
# pacman -> ghost <-
frames += pacman_right_ghost_left_frame
# ghost <-
frames += ghost_frames[1]
# pacman <-
frames += pacman_frames[1]
# ghost <- ghost ->
frames += ghost_frames[5]
# pacman <- ghost ->
frames += pacman_left_ghost_right_frame
# pacman ->
frames += pacman_frames[0]
# ghost ->
frames += ghost_frames[0]
# pacman <- pacman ->
frames += pacman_frames[5]
# ghost ->
frames += ghost_frames[2]
# pacman dies
frames += death_frames


im = frames[0]
im.save("anim_generated.gif",save_all=True, background=0, append_images=frames)

