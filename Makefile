
WAV_FILES=$(wildcard *.wav)
TARGETS=$(WAV_FILES:.wav=.raw)

all: $(TARGETS)

%.raw: %.wav
	sox $< -b 8 -r 11025 -t raw $@


animated_mod: merge_anim_mod.py pacman.mod anim_generated.gif anim2.mod
	python merge_anim_mod.py pacman.mod anim_generated.gif anim2.mod
