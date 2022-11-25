#!/home/recoder/.virtualenvs/pdfmagic/bin/python
import argparse
import time
from pathlib import Path
# from create_ean_line import GEN_START, GEN_STOP
from fpdf import FPDF
import data_from_excelsheet as exS

from helper_functions.datamatrixgen import create_one_dmtx_from_code


starttime = time.time()
print("starting...")

DMTX_FILES = "data/dmtx/"

DESIRED_FORMAT = (190, 45)
TEXT_POSITION = (32, 32)
DATAMATRIX_SIZE = (40, 40)
ARROW_SIZE = (25, 25)

MARGIN = 2
BLEED = 2
TEXT_POSITION = TEXT_POSITION[0] + BLEED, TEXT_POSITION[1] + BLEED
resultFormat = (DESIRED_FORMAT[0] + 2 * BLEED, DESIRED_FORMAT[1] + 2 * BLEED)


def DeckSort(filename):
    code = filename[1:].split("-")
    code[1], code[2] = code[2], code[1]
    total = str(ord(filename[0])) + "".join(code)
    return int(total)


def biNumToInt(biNum):
    return int(biNum)


def addCutting(sourcePdf):
    # TODO add spot color for cutting
    pass  # sourcePdf.setDrawSpotColor('opos',100)


def getCodes(fileName):
    import pickle

    exportNames = []
    codes_list = pickle.load(open(fileName, "rb"))
    for keys, codes in codes_list.items():
        exportNames.extend(codes)
    return exportNames


def returnCodesWithBeggining(wholeList, firstLetter):
    namesToReturn = []
    for oneName in wholeList:
        if oneName[0] in firstLetter:
            namesToReturn.append(oneName)
    return namesToReturn


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--rows", type=int, default=1, help="number of rows")
# # parser.add_argument('--file', dest='accumulate', action='store_const',
# #                     const=sum, nargs="?", default=max,
#                     help='sum the integers (default: find the max)')
parser.add_argument("-f", "--fileopen", dest="file_to_open", default="dumped_codes")

args = parser.parse_args()

pdf = FPDF(orientation="P", unit="mm", format=resultFormat)

pdf.set_font("Helvetica", style="B", size=36)
pdf.set_text_color(0, 0, 0)  # text set to black

pdf.set_line_width(1)  # box bounding
# dmtxFiles = exS.get_lost_values_list(excelSheet='missing_labels.xlsx', lines=54)
sticker_name = []
from data_from_excelsheet import prepair_data_for_generation
snames_data = prepair_data_for_generation(excelSheet="stow/regalyVB.xlsx")

snames=[]
for data in snames_data:
    snames.extend(snames_data[data])

snames.sort(key=DeckSort)
# partDMTX = returnCodesWithBeggining(dmtxFiles, ['G','H','I'])

for xth, imageName in enumerate(snames):

    firstLetter = imageName[0]

    horizontalPositon = int(imageName[8])
    print(imageName, horizontalPositon)

    pdf.add_page()
    # pdf.set_fill_color(0,0,0)

    pdf.set_fill_color(255, 255, 115)  # zluty podklad
    pdf.rect(0, 0, resultFormat[0], resultFormat[1], style="F")

    if horizontalPositon == 1:
        # DOWN
        # First Letter
        pdf.set_font("Helvetica", style="B", size=65)
        pdf.text(
            resultFormat[0] - 21 - BLEED - MARGIN, 18 + BLEED + MARGIN, firstLetter
        )

        # Main code text
        pdf.set_font("Helvetica", style="B", size=80)
        pdf.text(TEXT_POSITION[0] + (MARGIN * 5) + BLEED, TEXT_POSITION[1], imageName[1:])

        # Arrow
        pdf.image(
            "./aux_files/arrowDown.png",
            x=resultFormat[0] - ARROW_SIZE[0] - MARGIN - BLEED,
            y=18 + BLEED,
            w=ARROW_SIZE[0],
            h=ARROW_SIZE[1],
        )

        # Datamatrix
        image = create_one_dmtx_from_code(imageName)
        image_path = Path(DMTX_FILES + imageName + ".png")
        image.save(image_path)
        pdf.image(
            str(image_path),
            x=MARGIN + BLEED,
            y=MARGIN + BLEED,
            w=DATAMATRIX_SIZE[0],
            h=DATAMATRIX_SIZE[1],
        )
        image_path.unlink()

    else:
        if horizontalPositon == 2:
            # UP
            # First Letter
            pdf.set_font("Helvetica", style="B", size=65)
            pdf.text(4 + MARGIN + BLEED, resultFormat[1] - MARGIN - BLEED, firstLetter)

            # Arrow
            pdf.image(
                "./aux_files/arrowUp.png",
                x=MARGIN + BLEED,
                y=MARGIN + BLEED,
                w=ARROW_SIZE[0],
                h=ARROW_SIZE[1],
            )
        else:
            # others which i s higher
            # First Letter
            pdf.set_font("Helvetica", style="B", size=100)
            pdf.text(MARGIN + BLEED, 40 - MARGIN - BLEED, firstLetter)

        # Main code text
        pdf.set_font("Helvetica", style="B", size=80)
        pdf.text(TEXT_POSITION[0], TEXT_POSITION[1], imageName[1:])

        # Datamatrix
        image = create_one_dmtx_from_code(imageName)
        image_path = Path(DMTX_FILES + imageName + ".png")
        image.save(image_path)
        pdf.image(
            str(image_path),
            x=resultFormat[0] - DATAMATRIX_SIZE[0] - MARGIN - BLEED,
            y=resultFormat[1] - DATAMATRIX_SIZE[1] - MARGIN - BLEED,
            w=DATAMATRIX_SIZE[0],
            h=DATAMATRIX_SIZE[1],
        )
        image_path.unlink()

    if (xth % 100) == 0:
        newtime = time.time()
        print(f"vygenerovano: {xth} za {newtime - starttime}")
        starttime = newtime

    if (xth % 1000) == 999:
        pdf.output("export/stow" + str(xth) + ".pdf", "F")
        pdf = FPDF(orientation="P", unit="mm", format=resultFormat)

pdf.output("export/stow-rest.pdf", "F")
