import treepoem

chars = list(map(chr, range(65, 84)))

for stage in chars:
    for line in range(1, 36):
        for stock in range(1,5):
            for position in range(1,6):
                code = stage + str(line).zfill(2) + '-' + str(stock).zfill(2) + '-' + str(position).zfill(2)
                print('workon: ' + code)
                image = treepoem.generate_barcode(barcode_type='datamatrix', data=code)
                image.convert('1').save('data/dmtx/' + code + '.png')
