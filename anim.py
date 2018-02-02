#
# Generate an animation in a .mod that will show when played in protracker
#

import sys
from PIL import Image, ImageSequence


class Channel(object):
    def __init__(self):
        self.instrument = 0
        self.period = 0
        self.effect = 0
        self.params = 0

    def __str__(self):
        str = "%s %s %s %s, " % (hex(self.instrument), hex(self.period), hex(self.effect), hex(self.params))
        return str

    def to_bytes(self):
        ba = bytearray()
        byte1 = (self.instrument & 0b11110000) | (self.period & 0b111100000000) >> 8
        byte2 = self.period & 0b11111111
        byte3 = (self.instrument & 0b1111) << 4 | (self.effect & 0b1111)
        byte4 = self.params
 
        ba.append(byte1)
        ba.append(byte2)
        ba.append(byte3)
        ba.append(byte4)
        return ba

class Row(object):
    def __init__(self):
        self.channels = []

    def __str__(self):
        str = ""
        for channel in self.channels:
            str += "%s" % (channel)
        return str

    def to_bytes(self):
        ba = bytearray()
        for channel in self.channels:
            ba += channel.to_bytes()
        return ba


class Pattern(object):
    def __init__(self):
        self.rows = []

    def __str__(self):
        str = ""
        for i in range(0, len(self.rows)):
            row = self.rows[i]
            str += "%s => %s\n" % (i, row)
        return str

    def to_bytes(self):
        ba = bytearray()
        for row in self.rows:
            ba += row.to_bytes()
        return ba

class Frame(object):
    def __init__(self):
        self.rows = self.create_empty_frame()

    def set_pixel(self, xpos, ypos):
        chn = xpos / 5
        mod = xpos % 5
        if mod == 0:
            # hi sample no
            self.rows[ypos].channels[chn].instrument |= 0x10
        elif mod == 1:
            # lo sample no
            self.rows[ypos].channels[chn].instrument |= 0x01
        elif mod == 2:
            # effect
            self.rows[ypos].channels[chn].effect = 0x1
        elif mod == 3:
            # effect data hi
            self.rows[ypos].channels[chn].params |= 0x10
        elif mod == 4:
            # effect data lo
            self.rows[ypos].channels[chn].params |= 0x1
        else:
            print "wtf: %s %s" % (mod, xpos)
            sys.exit(1)
       


    def create_empty_frame(self):
        '''
        Create an empty protracker frame
        '''
        frame = []
        for _ in range(0, 15):
            row = Row()
            for _ in range(0, 4):
                channel = Channel()
                channel.period = 0 
                channel.instrument = 0
                channel.effect = 0
                channel.params = 0
                row.channels.append(channel)
            frame.append(row)

        return frame

    def fix_jump(self, frame_no):
        pos = 15*(frame_no%4)+7
        next_pos = pos+15
        next_pattern = frame_no/4
        if next_pos > 64:
            # Go to next pattern
            next_pos = 7
            next_pattern += 1

        hibyte = next_pos / 10
        lobyte = next_pos % 10
        #print frame_no, pos, next_pos, hibyte, lobyte, next_pattern
        self.rows[7].channels[2].effect = 0xb
        self.rows[7].channels[2].params = next_pattern
        self.rows[7].channels[3].effect = 0xd
        self.rows[7].channels[3].params = (hibyte << 4) | lobyte


def add_frames(frames, pacmac_up_going_right):
    for gif_frame in pacmac_up_going_right:

        frame_no = len(frames)

        frame = Frame()

        for y in range(0, gif_frame.height):
            for x in range(0, gif_frame.width):
                pixel = gif_frame.getpixel((x, y))
                if pixel == 1:
                    frame.set_pixel(x, y)

        frame.fix_jump(frame_no)

        frames.append(frame)



with open("anim.mod", "rb") as input_file:
    data = bytearray(input_file.read())

# No sanity checks
songname = data[0:20]

# TODO
# samples

songlength = data[950]
restart_position = data[951]
pattern_sequence = data[952:952+128]
version_mark = data[1080:1080+4]

pattern_data = data

print "%s" % len(data)

print "songname: %s" % (songname)
print "songlength: %s" % (songlength)
print "restart_position: %s" % (restart_position)
print "pattern_sequence: %s" % (pattern_sequence)
print "version_mark: %s" % (version_mark)

patterns = []

current_pos = 1084
no = 0
while current_pos < len(pattern_data) - 64*4*4:
    pattern = Pattern()
    for _ in range(0, 64):
        row = Row()
        for _ in range(0, 4):
            instrument_period = pattern_data[current_pos] << 8
            current_pos += 1 
            instrument_period |= pattern_data[current_pos]
            current_pos += 1
            instrument_effect = pattern_data[current_pos]
            current_pos += 1
            effect_data = pattern_data[current_pos]
            current_pos += 1

            instrument = (instrument_period & 0b1111000000000000) >> 8
            instrument |= (instrument_effect & 0b11110000) >> 4
            period = (instrument_period & 0b111111111111)
            effect = (instrument_effect & 0b1111)

            channel = Channel()
            channel.instrument = instrument
            channel.period = period
            channel.effect = effect
            channel.params = effect_data

            row.channels.append(channel)

        pattern.rows.append(row)

    print "pattern: %s\n%s" % (no, pattern)
    no += 1

x = 0
x_inc = 1
y = 2
y_inc = 1

poslist = []


frames = []

gif = Image.open("img/animation.gif")

pacmac_up_going_right = []
#gif_frames = ImageSequence.Iterator(gif)
for gif_frame in ImageSequence.Iterator(gif):
    pacmac_up_going_right.append(gif_frame.copy())

pacmac_up_going_left = []
for gif_frame in pacmac_up_going_right:
    gif_frame = gif_frame.transpose(Image.FLIP_LEFT_RIGHT)
    pacmac_up_going_left.append(gif_frame.copy())

pacman_down_going_right = []
for gif_frame in pacmac_up_going_right:
    new_frame = Image.new(gif_frame.mode, gif_frame.size)
    new_frame.paste(gif_frame, (0, 8))
    pacman_down_going_right.append(new_frame)

pacman_down_going_left = []
for gif_frame in pacmac_up_going_left:
    new_frame = Image.new(gif_frame.mode, gif_frame.size)
    new_frame.paste(gif_frame, (0, 8))
    pacman_down_going_left.append(new_frame)


add_frames(frames, pacmac_up_going_right)
add_frames(frames, pacman_down_going_right)
add_frames(frames, pacmac_up_going_left)
add_frames(frames, pacman_down_going_left)


while len(frames) % 4 != 0:
    frame_no = len(frames)
    frame = Frame()
    frame.fix_jump(frame_no) 
    frames.append(frame)

frames[0].rows[0].channels[0].effect = 0xf
frames[0].rows[0].channels[0].params = 0x3


# Test, generate X frames
# One frame is 15 rows
#frames = []
#for i in range(0, 124):
#    frame = []
#    for _ in range(0, 15):
#        row = Row()
#        for _ in range(0, 4):
#            channel = Channel()
#            channel.period = 0 
#            channel.instrument = 0
#            channel.effect = 0
#            channel.params = 0
#            row.channels.append(channel)
#        frame.append(row)

#    poslist.insert(0, (x,y))
#    if len(poslist) > 5:
#        poslist.pop()

#    for xpos,ypos in poslist:
#        chn = xpos / 5
#        mod = xpos % 5
#        if mod == 0:
            # hi sample no
#            frame[ypos].channels[chn].instrument = 0x10
#        elif mod == 1:
            # lo sample no
#            frame[ypos].channels[chn].instrument = 0x01
#        elif mod == 2:
            # effect
#            frame[ypos].channels[chn].effect = 0x1
#        elif mod == 3:
            # effect data hi
#            frame[ypos].channels[chn].params = 0x10
#        elif mod == 4:
            # effect data lo
#            frame[ypos].channels[chn].params = 0x1
#        else:
#            print "wtf: %s %s" % (mod, xpos)
#            sys.exit(1)

#    pos = 15*(i%4)+7
#    next_pos = pos+15
#    next_pattern = i/4
#    if next_pos > 64:
        # Go to next pattern
#        next_pos = 7
#        next_pattern += 1

#    hibyte = next_pos / 10
#    lobyte = next_pos % 10
#    print i, pos, next_pos, hibyte, lobyte, next_pattern
#    frame[7].channels[2].effect = 0xb
#    frame[7].channels[2].params = next_pattern
#    frame[7].channels[3].effect = 0xd
#    frame[7].channels[3].params = (hibyte << 4) | lobyte

#    frames.append(frame)

#    x += x_inc
#    y += y_inc
#    if x < 0:
#        x = 0
#        x_inc = -x_inc
#    if x >= 5*4:
#        x = 5*4-1
#        x_inc = -x_inc
#    if y < 0:
#        y = 0
#        y_inc = -y_inc
#    if y >= 15:
#        y = 15-1
#        y_inc = -y_inc

    
new_patterns = []

pattern = Pattern()
for frame in frames:
    for row in frame.rows:
        pattern.rows.append(row)
    if len(pattern.rows) == 15*4:
        while len(pattern.rows) < 64:
            row = Row()
            for _ in range(0, 4):
                row.channels.append(Channel())
            pattern.rows.append(row)
        new_patterns.append(pattern)
        pattern = Pattern()


for i in range(0, len(new_patterns)):
    data[952+i] = i

data[950] = len(new_patterns)

with open("anim2.mod", "wb") as output_file:
    output_file.write(data[0:1084])
    for pattern in new_patterns:
        output_file.write(pattern.to_bytes())



