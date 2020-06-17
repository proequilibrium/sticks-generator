"""
    modul for generating datamatrix
"""

#!/home/recoder/.virtualenvs/pdfmagic/bin/python
import time
import pickle
#from create_ean_line import GEN_START, GEN_STOP
from fpdf import FPDF
print('script zacina loaduji knihovny...')

starttime = time.time()
print("generujeme")

DEFINED_SIZE = (80, 70)

DATAMATRIX_SIZE = (25, 25)

SMALL_BOX_FROM_TOP = 38
SMALL_BOX_HEIGHT = 4
SMALL_BOX_GAP = 2

COMPLETE_CODES_BATCH = [[19]]

MARGIN = 4
BLEED = 2
SIDE = MARGIN + BLEED

DMTX_FILES = 'data/dmtx/'

RESULT_FORMAT = (DEFINED_SIZE[0] + 2*BLEED, DEFINED_SIZE[1] + 2*BLEED)
codePosition = (SIDE + 2, 35)


def deck_sort(filename):
    """
        different sort for codes
    """
    code = filename[1:].split('-')
    code[1], code[2] = code[2], code[1]
    total = str(ord(filename[0])) + ''.join(code)
    return int(total)


def draw_rect_return_datam_position(page, num_positions, pos_to_color):
    """
        drawing slelcted rectangle and return position for datamatrix
    """
    box_width = int(
        (RESULT_FORMAT[0]-(SMALL_BOX_GAP * (num_positions-1)) -
         2*SIDE) / num_positions
    )
    pdf.set_fill_color(255, 0, 0)  # Red fill

    for nth in range(num_positions):
        style = 'D'
        if (nth + 1) == pos_to_color:
            style = 'FD'

        page.rect(SIDE + (nth*(box_width + SMALL_BOX_GAP)),
                  SMALL_BOX_FROM_TOP,
                  box_width,
                  SMALL_BOX_HEIGHT,
                  style=style)

    half_red_rect = SIDE + ((pos_to_color - 1) *
                            (box_width + SMALL_BOX_GAP)) + (box_width / 2)
    teor_position = half_red_rect - (DATAMATRIX_SIZE[0] / 2)
    rigth_bound = RESULT_FORMAT[0] - DATAMATRIX_SIZE[0] - SIDE
    return min(max(teor_position, SIDE-1), rigth_bound)


def get_stack(cell_val):
    """
        parse cell val
    """
    return (cell_val[:3], int(cell_val[4:6]), int(cell_val[7:9]))


def get_stack_pos(cell_val):
    """
        parse cell val return Stack
    """
    return int(cell_val[4:6])


def get_stack_level(cell_val):
    """
        parse cell return stack level
    """
    return int(cell_val[7:9])


def get_num_stacks(codes_list):
    """
        magicaly return number of stacks
    """
    nums = {}
    for stages in range(1, 4*5+1):
        nums[stages] = 0
    for codes in codes_list.values():
        nums[len(codes)] += 1
    return nums


def get_codes_with_exact_num(exact_num):
    """
        filter codes
    """
    export_name = []
    export_stage_sizes = {}
    codes_list = pickle.load(open('dumped_codes', 'rb'))
    for stage_key, codes in codes_list.items():
        if len(codes) in exact_num:
            export_name.extend(codes)
            export_stage_sizes[stage_key] = 0
            for code in codes:
                export_stage_sizes[stage_key] = max(
                    int(code[4:6]), export_stage_sizes[stage_key])
    return (export_name, export_stage_sizes)


def draw_blue_line(source_page, stage_code):
    """
        Draw blue line
    """
    source_page.set_fill_color(0, 255, 255)  # Horni modry
    source_page.rect(0, 0, RESULT_FORMAT[0], 15 + SIDE, style='F')
    source_page.set_font('Helvetica', style="B", size=50)
    source_page.text(SIDE, 12 + SIDE, stage_code)


def add_datamatrix(source_page, x_position, datamatrix_name):
    """
        add datamatrix to pdf
    """
    source_page.image("./data/dmtx/" + str(datamatrix_name) + ".png",
                      x=x_position,
                      y=RESULT_FORMAT[1] - DATAMATRIX_SIZE[1] - SIDE + 1.5,
                      w=DATAMATRIX_SIZE[0],
                      h=DATAMATRIX_SIZE[1])


if __name__ == "__main__":
    for codesBatch in COMPLETE_CODES_BATCH:
        pdf = FPDF(orientation="P", unit='mm', format=RESULT_FORMAT)

        pdf.set_font('Helvetica', style='B', size=36)
        pdf.set_text_color(0, 0, 0)  # text set to black
        pdf.set_line_width(1.5)  # box bounding

        codesString, stageSizes = get_codes_with_exact_num(codesBatch)
        codesString.sort(key=deck_sort)  # setrideni

        STAGE = ''

        for xth, codeString in enumerate(codesString):
            # if xth > (1000):
            #     print('FORCED BREAK')
            #     break

            # veariables for code parts
            stageLetter = codeString[0]
            STAGE = codeString[:3]
            codeWithoutLetter = codeString[1:]
            positionOnLevel = int(codeString[4:6])
            levelAtStage = int(codeString[7:])

            print(codeString, codeString[8])
            if levelAtStage > 2:
                pdf.add_page()
                # pdf.set_fill_color(0,0,0)

                draw_blue_line(pdf, stageLetter)

                pdf.set_font('Helvetica', style="B", size=48)
                pdf.text(codePosition[0], codePosition[1], codeWithoutLetter)

                datamatrixX = draw_rect_return_datam_position(
                    pdf, stageSizes[STAGE], positionOnLevel)

                add_datamatrix(pdf, datamatrixX, codeString)

                if (xth % 1000) == 999:
                    pdf.output("export/square/datamatrix-" + str(xth) +
                               ''.join(str(codesBatch).split(' ')) + ".pdf", "F")
                    print(f'Ukladam {xth} pdf {time.time() - starttime}')
                    starttime = time.time()
                    pdf = FPDF(orientation="P", unit='mm',
                               format=RESULT_FORMAT)

                    pdf.set_font('Helvetica', style='B', size=36)
                    pdf.set_text_color(0, 0, 0)  # text set to black
                    pdf.set_line_width(1.5)  # box bounding

        pdf.output("export/square/datamatrix-" +
                   "".join(str(codesBatch).split(' ')) + "-last.pdf", "F")
