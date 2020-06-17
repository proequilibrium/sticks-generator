#!/home/recoder/.virtualenvs/pdfmagic/bin/python
import argparse
import time
import os
#from create_ean_line import GEN_START, GEN_STOP
from fpdf import FPDF
import dataFromExcelsheet as exS

print('script zacina loaduji knihovny...')

starttime = time.time()
print("zaciname")

desFormat = (190, 45)
textPosition = (32, 32)
datamatrixSize = (40, 40)
arrowSize = (25, 25)

margin = 2
bleed = 2
textPosition = textPosition[0] + bleed, textPosition[1] + bleed
resultFormat = (desFormat[0]+2*bleed, desFormat[1]+2*bleed)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('rows', type=int, default=1,
                    help='number of rows')
parser.add_argument('-f', '--filopen', dest='file_to_open',
                    action='store_true', default='cagobelo')


def DeckSort(filename):
    code = filename[1:].split('-')
    code[1], code[2] = code[2], code[1]
    total = str(ord(filename[0])) + ''.join(code)
    return int(total)


def biNumToInt(biNum):
    return int(biNum)


def addCutting(sourcePdf):
    pass  # sourcePdf.setDrawSpotColor('opos',100)


def getCodes(fileName):
    import pickle
    exportNames = []
    codes_list = pickle.load(open(fileName, 'rb'))
    for keys, codes in codes_list.items():
        exportNames.extend(codes)
    return exportNames


def returnCodesWithBeggining(wholeList, firstLetter):
    namesToReturn = []
    for oneName in wholeList:
        if oneName[0] in firstLetter:
            namesToReturn.append(oneName)
    return namesToReturn


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('rows', type=int, default=1,
                    help='number of rows')
# # parser.add_argument('--file', dest='accumulate', action='store_const',
# #                     const=sum, nargs="?", default=max,
#                     help='sum the integers (default: find the max)')
parser.add_argument('-f', '--filopen', dest='file_to_open',
                    action='store_true', default='dumped_codes')

args = parser.parse_args()

pdf = FPDF(orientation="P", unit='mm', format=resultFormat)

pdf.set_font('Helvetica', style='B', size=36)
pdf.set_text_color(0, 0, 0)  # text set to black

pdf.set_line_width(1)  # box bounding
dmtxFiles = exS.get_lost_values_list(excelSheet='missing_labels.xlsx', lines=54)
dmtxFiles.sort(key=DeckSort)
partDMTX = dmtxFiles
#partDMTX = returnCodesWithBeggining(dmtxFiles, ['G','H','I'])

for xth, imageName in enumerate(partDMTX):

    firstLetter = imageName[0]
    if firstLetter == 'I':
        firstLetter = " I"

    horizontalPositon = int(imageName[8])
    print(imageName, horizontalPositon)

    pdf.add_page()
    # pdf.set_fill_color(0,0,0)

    pdf.set_fill_color(255, 255, 115)  # zluty podklad
    pdf.rect(0, 0, resultFormat[0], resultFormat[1], style='F')

    if horizontalPositon == 1:
        # DOWN
        # First Letter
        pdf.set_font('Helvetica', style="B", size=65)
        pdf.text(resultFormat[0] - 21 - bleed - margin,
                 18 + bleed + margin, firstLetter)

        # Main code text
        pdf.set_font('Helvetica', style="B", size=80)
        pdf.text(textPosition[0]+(margin*5)+bleed,
                 textPosition[1], imageName[1:])

        # Arrow
        pdf.image("./arrowDown.png",
                  x=resultFormat[0]-arrowSize[0]-margin-bleed,
                  y=18 + bleed,
                  w=arrowSize[0],
                  h=arrowSize[1])

        # Datamatrix
        pdf.image("./data/dmtx/" + str(imageName) + ".png",
                  x=margin+bleed,
                  y=margin+bleed,
                  w=datamatrixSize[0],
                  h=datamatrixSize[1])

    else:
        if horizontalPositon == 2:
            # UP
            # First Letter
            pdf.set_font('Helvetica', style="B", size=65)
            pdf.text(4 + margin + bleed,
                     resultFormat[1] - margin - bleed, firstLetter)

            # Arrow
            pdf.image("./arrowUp.png",
                      x=margin + bleed,
                      y=margin + bleed,
                      w=arrowSize[0],
                      h=arrowSize[1])
        else:
            # others which i s higher
            # First Letter
            pdf.set_font('Helvetica', style="B", size=100)
            pdf.text(margin + bleed, 40 - margin - bleed, firstLetter)

        # Main code text
        pdf.set_font('Helvetica', style="B", size=80)
        pdf.text(textPosition[0], textPosition[1], imageName[1:])

        # Datamatrix
        pdf.image("./data/dmtx/" + str(imageName) + ".png",
                  x=resultFormat[0]-datamatrixSize[0]-margin-bleed,
                  y=resultFormat[1]-datamatrixSize[1]-margin-bleed,
                  w=datamatrixSize[0],
                  h=datamatrixSize[1])

    if (xth % 100) == 0:
        newtime = time.time()
        print(f"vygenerovano: {xth} za {newtime - starttime}")
        starttime = newtime

    if (xth % 1000) == 999:
        pdf.output("export/datamatrix-dodelavka" + str(xth) + ".pdf", "F")
        pdf = FPDF(orientation="P", unit='mm', format=resultFormat)

pdf.output("export/datamatrix-dodelavka.pdf", "F")
