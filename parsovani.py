import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('rows', type=int, default=1,
                    help='number of rows')
# # parser.add_argument('--file', dest='accumulate', action='store_const',
# #                     const=sum, nargs="?", default=max,
#                     help='sum the integers (default: find the max)')
parser.add_argument('-f', '--filopen', dest='file_to_open',
                    action='store_true', default='cagobelo')

args = parser.parse_args()

print(f'row {args.rows} file {args.file_to_open}')
