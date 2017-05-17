#!/usr/bin/env python

import sys
from optparse import OptionParser
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", 24)

usage = "makebingo.py [options] gridContentFile1.csv [gridContentFile2.csv]"
parser = OptionParser(usage = usage)
parser.add_option("-W", "--width", dest="gridWidth",
                  help="Grid Width", default = 9, type="int")
parser.add_option("-H", "--height", dest="gridHeight",
                  help="Grid height", default = 4, type = "int")
parser.add_option("-e", "--empty", dest="emptyCases",
                  help="Empty Cases", default = 12, type = "int")
parser.add_option("-n", "--number", dest="gridCount",
                  help="Number of grids to generate", default = 1, type = "int")
parser.add_option("-C", "--CSV_SEPARATOR", dest="csvSep",
                  help="Separator for input CSV files", default = ';')

SLOT_SIDE = 200
INTERLINE = .5

(options, args) = parser.parse_args()
if len(args) == 0:
    print (usage)
    sys.exit(1)

Slots = []

class GridSlot:
    def __init__(self, value, points = 1):
        self.value = value
        self.points = int(points)

    def paint(self, w, h):
        output = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(output)
        draw.rectangle([(0, 0), (w, h)], fill = (255, 255, 255), outline = (0, 0, 0))

        texts = []
        words = [wo.decode('UTF-8') for wo in self.value.split(' ')]
        value = " " + words.pop(0)

        while len(words) > 0:
            newWord = words.pop(0)
            if font.getsize(value + ' ' + newWord)[0] < w * .9:
                value += " " + newWord
            else:
                texts.append(value)
                value = " " + newWord

        if len(value)>0:
            texts.append(value)

        _, textH = font.getsize(texts[0])
        for tInd, text in enumerate(texts):
            draw.text((0, tInd * textH * (1 + INTERLINE)),text,(0,0,0),font=font)

        return output

class EmptyGridSlot:
    def paint(self, w, h):
        output = Image.new("RGB", (w, h))
        return output

for csv_slots in args:
    fIn = open(csv_slots)
    line = fIn.readline()
    while line != "":
        data = line.rstrip('\n').split(options.csvSep)
        Slots.append(GridSlot(*data))
        line = fIn.readline()

if len(Slots) + options.emptyCases < options.gridWidth * options.gridHeight:
    print ("Unsufficent grid content for size " + str(options.gridWidth) + "x" + str(options.gridHeight))
    sys.exit(1)

for gridInd in range(options.gridCount):
    gridSlots = [EmptyGridSlot() for i in range(options.emptyCases)]
    gridSlots += random.sample(Slots, options.gridWidth * options.gridHeight - options.emptyCases)
    random.shuffle(gridSlots)

    output = Image.new("RGB", (options.gridWidth * SLOT_SIDE, options.gridHeight * SLOT_SIDE))

    for y in range(options.gridHeight):
        for x in range(options.gridWidth):
            slot = gridSlots.pop()
            slotImage = slot.paint(SLOT_SIDE, SLOT_SIDE)
            output.paste(slotImage, (x * SLOT_SIDE, y * SLOT_SIDE))

    output.save("./grid_" + str(gridInd) + ".png")
