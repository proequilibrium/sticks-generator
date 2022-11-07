import argparse
import treepoem


def prepair_code(stage, line, stock, position):
    return (
        stage + str(line).zfill(2) + "-" + str(stock).zfill(2) + "-" + str(position).zfill(2)
    )

def get_datamatrix_from_string(code: str):
        return treepoem.generate_barcode(barcode_type="datamatrix", data=code)

def create_one_dmtx(stage: str, line: str, stock:str, position: str):
    """_summary_

    Args:
        stage (_type_): _description_
        line (_type_): _description_
        stock (_type_): _description_
        position (_type_): _description_

    Returns:
        _type_: _description_
    """

    code = prepair_code(stage, line, stock, position)
    image = get_datamatrix_from_string(code)
    image = image.convert("L")
    return image, code

def create_one_dmtx_from_code(code: str):
    """_summary_

    Args:
        stage (_type_): _description_
        line (_type_): _description_
        stock (_type_): _description_
        position (_type_): _description_

    Returns:
        _type_: _description_
    """
    image = get_datamatrix_from_string(code)
    image = image.convert("L")
    return image


def create_one_dmtx_png(stage, line, stock, position, path: str="data/dmtx/"):
    image, code = create_one_dmtx(stage, line, stock, position)
    image.save(f"{path}{code}.png")


def generate_for_all_images():
    """ Gerneate all images for all possible combinations of stage, line, stock and position
    Args:
    Returns:
    Exceptions:
    """
    chars = list(map(chr, range(88, 89)))

    for stage in chars:
        for line in range(1, 36):
            for stock in range(1, 5):
                for position in range(1, 6):
                    code = prepair_code(stage, line, stock, position)
                    image = get_datamatrix_from_string(code)
                    image.save(f"data/dmtx/{code}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--stage", type=str, default="F", help="Stage")
    parser.add_argument("-l", "--line", type=int, default=1, help="Line")
    parser.add_argument("-s", "--stock", type=int, default=1, help="Stock")
    parser.add_argument("-p", "--position", type=int, default=1, help="Position")
    parser.add_argument("-o", "--output", type=str, default="data/dmtx/", help="Output path")
    args = parser.parse_args()
    create_one_dmtx_png(args.stage, args.line, args.stock, args.position, args.output)
