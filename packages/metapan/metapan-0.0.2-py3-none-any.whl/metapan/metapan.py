import argparse
import sys
import logging
import traceback
import os
from multiprocessing import Queue, Process, cpu_count

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

def mainFunction(args):
    print(hello)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # use bpga2 section
    files = subparsers.add_parser("main", help="main function for metapan")
    files.add_argument('-i', metavar='InputFileDirectory',dest='InputFileDirectory', required=True,
                       help='Enter path to input directory containing fasta file')
    files.add_argument('-o', metavar='OutputFile',dest='OutputFile', required=True,
                       help='Enter name for input File')
    files.add_argument('-m', metavar='Metadatafile',dest='Metadatafile', required=True,
                       help='Enter name for input File')
    files.add_argument('-t', metavar='threads',dest='threads', default=cpu_count(),
                       help='Enter number of threads')
    files.set_defaults(func=mainFunction)

       # Get all arguments
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_help()
        parser.exit()

    pass
if __name__ == '__main__':
	main()
