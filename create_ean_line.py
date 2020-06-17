# import importlib.util
# spec = importlib.util.spec_from_file_location('barcodex',"./barcode/base.py")
# barcodexmodule = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(barcodexmodule)

#from python_barcode.barcode.base import Barcode
import barcode
# image writer
from barcode.writer import ImageWriter

import barcode
import time

GEN_NUM = 4000
GEN_START = 8000
GEN_STOP = GEN_START + GEN_NUM
#show available barcodes
#print(barcode.PROVIDED_BARCODES)
#init barcode constructor

starttime = time.time()

EAN = barcode.get_barcode_class('ean8')
#generate barcode with image writer
for code in range(GEN_START, GEN_STOP + 1):
    ean_produced = EAN(str(code).zfill(7), writer = ImageWriter())
    #save to png file
    if (code % 100) == 0:
        newtime = time.time()
        print(f"vygenerovano png: {code} za {newtime - starttime}")
        starttime = newtime
    fullname = ean_produced.save('./data/bar-'+str(code))
# EAN = barcode.get_barcode_class('ean8')
# #generate barcode with image writer
# for code in range(GEN_START, GEN_STOP + 1):
#     ean_produced = EAN(str(code).zfill(8))
#     #save to png file
#     fullname = ean_produced.save('./data/bar-'+str(code))
