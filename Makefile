
WAV_FILES=$(wildcard *.wav)
TARGETS=$(WAV_FILES:.wav=.raw)

all: $(TARGETS)

%.raw: %.wav
	sox $< -b 8 -r 11025 -t raw $@


