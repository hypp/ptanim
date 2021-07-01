#
# Merge an animation into a .mod that will show when played in protracker
#

import sys
from PIL import Image, ImageSequence
import argparse

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

def add_frame(frames, gif_frame):
    '''
    Add one gif frame to the frames list
    '''
    frame_no = len(frames)

    frame = Frame()

    for y in range(0, gif_frame.height):
        for x in range(0, gif_frame.width):
            pixel = gif_frame.getpixel((x, y))
            if pixel == 1:
                frame.set_pixel(x, y)

    frame.fix_jump(frame_no)

    frames.append(frame)

def add_frames(frames, gif_frames):
    '''
    Add list of gif frames to the frames list
    '''
    for gif_frame in gif_frames:
        add_frame(frames, gif_frame)


parser = argparse.ArgumentParser(description='Merge a ProTracker mod and an animation')

parser.add_argument('--verbose', '-v', action='store_true', help='Write more information to stdout')
parser.add_argument('inputmodfile', metavar='<inputmodfile>', help='Modfile to convert')
parser.add_argument('inputgiffile', metavar='<inputgiffile>', help='Giffile to convert')
parser.add_argument('outputmodfile', metavar='<outputmodfile>', help='Modfile to create')

args = parser.parse_args()

inmod = args.inputmodfile
outmod = args.outputmodfile
ingif = args.inputgiffile
verbose = args.verbose

with open(inmod, "rb") as input_file:
    data = bytearray(input_file.read())

# No sanity checks
songname = data[0:20]

songlength = data[950]
restart_position = data[951]
pattern_sequence = data[952:952+128]
max_pattern = 0
for no in pattern_sequence:
    if no > max_pattern:
        max_pattern = no
num_patterns = max_pattern+1
version_mark = data[1080:1080+4]
# Fix format for > 64 patterns
data[1080+1] = "!"
data[1080+3] = "!"

pattern_data = data

if verbose:
    print "%s" % len(data)

    print "songname: %s" % (songname)
    print "songlength: %s" % (songlength)
    print "restart_position: %s" % (restart_position)
    print "pattern_sequence: %s" % (pattern_sequence)
    print "version_mark: %s" % (version_mark)

patterns = []

current_pos = 1084
no = 0
for no in range(0, num_patterns):
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

    patterns.append(pattern)
    #print "pattern: %s\n%s" % (no, pattern)

samples_start = current_pos

frames = []

gif = Image.open(ingif)

for gif_frame in ImageSequence.Iterator(gif):
    add_frame(frames, gif_frame)

while len(frames) < 101*4:
    # Add empty frames
    frame_no = len(frames)
    frame = Frame()
    frame.fix_jump(frame_no) 
    frames.append(frame)

frames[0].rows[0].channels[0].effect = 0xf
frames[0].rows[0].channels[0].params = 0x3

if verbose:
    print "len: %s" % (len(frames))
    
# Grab one row from the original patterns
# and store it at pos 7 in the frames
play_position = 0
pattern_position = 0
for frame in frames:
    current_pattern = patterns[pattern_sequence[play_position]]
    row = current_pattern.rows[pattern_position]

    frame.rows[7].channels[0].period = row.channels[3].period
    frame.rows[7].channels[0].instrument = row.channels[3].instrument
    if row.channels[3].effect == 0xd:
        frame.rows[7].channels[0].effect = 0
        pattern_position = 63
    else:
        frame.rows[7].channels[0].effect = row.channels[3].effect
    frame.rows[7].channels[0].params = row.channels[3].params

    frame.rows[7].channels[1].period = row.channels[2].period
    frame.rows[7].channels[1].instrument = row.channels[2].instrument
    if row.channels[2].effect == 0xd:
        frame.rows[7].channels[1].effect = 0
        pattern_position = 63
    else:
        frame.rows[7].channels[1].effect = row.channels[2].effect
    frame.rows[7].channels[1].params = row.channels[2].params

    frame.rows[7].channels[2].period = row.channels[1].period
    frame.rows[7].channels[2].instrument = row.channels[1].instrument
    if row.channels[1].effect == 0xd:
        pattern_position = 63

    frame.rows[7].channels[3].period = row.channels[0].period
    frame.rows[7].channels[3].instrument = row.channels[0].instrument
    if row.channels[0].effect == 0xd:
        pattern_position = 63

    pattern_position += 1
    if pattern_position > 63:
        pattern_position = 0
        play_position += 1
        if play_position >= songlength:
            play_position = restart_position


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


if len(new_patterns) > 100:
    new_patterns = new_patterns[:100]

# Stop song
new_patterns[-1].rows[52].channels[0].effect = 0xf
new_patterns[-1].rows[52].channels[0].params = 0x0

# Generate new song sequence
for i in range(0, len(new_patterns)):
    data[952+i] = i

data[950] = len(new_patterns)+1

with open(outmod, "wb") as output_file:
    output_file.write(data[0:1084])
    for pattern in new_patterns:
        output_file.write(pattern.to_bytes())
    output_file.write(data[samples_start:])



