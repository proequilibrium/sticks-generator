"""
    modul for generating datamatrix
"""

#!/home/recoder/.virtualenvs/pdfmagic/bin/python
import time
import pickle
from pathlib import Path

# from create_ean_line import GEN_START, GEN_STOP
from fpdf import FPDF
from data_from_excelsheet import prepair_data_for_generation

from helper_functions.datamatrixgen import create_one_dmtx_from_code

starttime = time.time()
print("Starting ....")

DEFINED_SIZE = (80, 70)

DATAMATRIX_SIZE = (25, 25)

SMALL_BOX_FROM_TOP = 38
SMALL_BOX_HEIGHT = 4
SMALL_BOX_GAP = 2

COMPLETE_CODES_BATCH = [[19]]

MARGIN = 4
BLEED = 2
SIDE = MARGIN + BLEED

DMTX_FILES = "data/dmtx/"

RESULT_FORMAT = (DEFINED_SIZE[0] + 2 * BLEED, DEFINED_SIZE[1] + 2 * BLEED)
codePosition = (SIDE + 2, 35)


def deck_sort(filename):
    """
    different sort for codes
    """
    code = filename[1:].split("-")
    code[1], code[2] = code[2], code[1]
    total = str(ord(filename[0])) + "".join(code)
    return int(total)


def draw_rect_return_datam_position(page, num_positions, pos_to_color):
    """
    drawing slelcted rectangle and return position for datamatrix
    """
    box_width = int(
        (RESULT_FORMAT[0] - (SMALL_BOX_GAP * (num_positions - 1)) - 2 * SIDE)
        / num_positions
    )
    pdf.set_fill_color(255, 0, 0)  # Red fill

    for nth in range(num_positions):
        style = "D"
        if (nth + 1) == pos_to_color:
            style = "FD"

        page.rect(
            SIDE + (nth * (box_width + SMALL_BOX_GAP)),
            SMALL_BOX_FROM_TOP,
            box_width,
            SMALL_BOX_HEIGHT,
            style=style,
        )

    half_red_rect = (
        SIDE + ((pos_to_color - 1) * (box_width + SMALL_BOX_GAP)) + (box_width / 2)
    )
    teor_position = half_red_rect - (DATAMATRIX_SIZE[0] / 2)
    rigth_bound = RESULT_FORMAT[0] - DATAMATRIX_SIZE[0] - SIDE
    return min(max(teor_position, SIDE - 1), rigth_bound)


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


def get_stage_id(cell_vall):
    """
    return stage id
    """
    return cell_vall[:3]


def get_num_stacks(codes_list):
    """
    magicaly return number of stacks
    """
    nums = {}
    for stages in range(1, 4 * 5 + 1):
        nums[stages] = 0
    for codes in codes_list.values():
        nums[len(codes)] += 1
    return nums


def get_codes_with_exact_num(exact_num):
    """
    filter codes
    """
    export_name = []
    export_stage_sizes = {}  # tuple name of stage
    with open("dumped_codes", "r") as code_file:
        export_name = code_file.read().splitlines()
        for cell_val in export_name:
            stage_key = get_stage_id(cell_val)
            if stage_key in export_stage_sizes:
                export_stage_sizes[stage_key] = max(
                    get_stack_pos(cell_val), export_stage_sizes[stage_key]
                )
            else:
                export_stage_sizes[stage_key] = 1
        return (export_name, export_stage_sizes)


def get_stage_widths(stage_batches: dict):
    """
    filter codes
    """
    get_stage_widths = {}
    get_stage_offset = {}
    for stage_key, val in stage_batches.items():
        get_stage_widths[stage_key] = len(set([get_stack_pos(x) for x in val]))
        get_stage_offset[stage_key] = get_stage_widths[stage_key] - max(
            [get_stack_pos(x) for x in val]
        )
    return get_stage_widths, get_stage_offset


def draw_blue_line(source_page, stage_code):
    """
    Draw blue line
    """
    source_page.set_fill_color(0, 255, 255)  # Horni modry
    source_page.rect(0, 0, RESULT_FORMAT[0], 15 + SIDE, style="F")
    source_page.set_font("Helvetica", style="B", size=50)
    source_page.text(SIDE, 12 + SIDE, stage_code)


def add_datamatrix(source_page, x_position, datamatrix_name):
    """
    add datamatrix to pdf
    """
    image = create_one_dmtx_from_code(datamatrix_name)
    image_path = Path(DMTX_FILES + datamatrix_name + ".png")
    image.save(image_path)
    source_page.image(
        str(image_path),
        x=x_position,
        y=RESULT_FORMAT[1] - DATAMATRIX_SIZE[1] - SIDE + 1.5,
        w=DATAMATRIX_SIZE[0],
        h=DATAMATRIX_SIZE[1],
    )
    # remove image
    image_path.unlink()


# TODO
# def add_page(
#     pdf, codePosition, codeWithoutLetter, stageSizes, positionOnLevel, generated
# ):
#     if levelAtStage > 2:
#         pdf.add_page()
#         # pdf.set_fill_color(0,0,0)
#         generated += 1
#         draw_blue_line(pdf, stageLetter)

#         pdf.set_font("Helvetica", style="B", size=48)
#         pdf.text(codePosition[0], codePosition[1], codeWithoutLetter)

#         datamatrixX = draw_rect_return_datam_position(
#             pdf, stageSizes[STAGE], positionOnLevel
#         )

#         add_datamatrix_generated(pdf, datamatrixX, codeString)


if __name__ == "__main__":
    pdf = FPDF(orientation="P", unit="mm", format=RESULT_FORMAT)

    pdf.set_font("Helvetica", style="B", size=36)
    pdf.set_text_color(0, 0, 0)  # text set to black
    pdf.set_line_width(1.5)  # box bounding

    stages_codes = prepair_data_for_generation(excelSheet="stow/regalyVB.xlsx")
    stage_widths, stage_widths_ofset = get_stage_widths(stages_codes)
    workon_stage = ""
    generated = 0

    for xth, (stage, positions) in enumerate(stages_codes.items()):
        if xth > (50):
            print("FORCED BREAK")
            break

        # veariables for code parts
        for position in positions:
            stageLetter = position[0]
            codeWithoutLetter = position[1:]
            positionOnLevel = int(position[4:6])
            levelAtStage = int(position[7:])

            if stage != workon_stage:
                starttime = time.time()
                pdf.output(f"./export/square/datamatrix-{generated}-{stage}.pdf", "F")
                generated = 0
                print(f"Ukladam {xth} pdf {time.time() - starttime}")

                workon_stage = stage

                pdf = FPDF(orientation="P", unit="mm", format=RESULT_FORMAT)

                pdf.set_font("Helvetica", style="B", size=36)
                pdf.set_text_color(0, 0, 0)  # text set to black
                pdf.set_line_width(1.5)  # box bounding

            print(position, position[8])
            if levelAtStage > 2:
                pdf.add_page()
                # pdf.set_fill_color(0,0,0)
                generated += 1
                draw_blue_line(pdf, stageLetter)

                pdf.set_font("Helvetica", style="B", size=48)
                pdf.text(codePosition[0], codePosition[1], codeWithoutLetter)

                datamatrixX = draw_rect_return_datam_position(
                    pdf,
                    stage_widths[stage],
                    positionOnLevel + stage_widths_ofset[stage],
                )

                add_datamatrix(pdf, datamatrixX, position)

        pdf.output(
            "export/square/datamatrix-"
            + "".join(str(stage).split(" "))
            + "-221108.pdf",
            "F",
        )
