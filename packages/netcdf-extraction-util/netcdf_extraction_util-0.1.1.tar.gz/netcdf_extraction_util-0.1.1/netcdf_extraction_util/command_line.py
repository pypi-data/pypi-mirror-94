from netcdf_extraction_util import netcdf_extraction
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_nc", help="netcdf file containing the time-series")
    parser.add_argument("reach_id", help="reach id to extract", type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    input_nc = args.input_nc
    reach_id = args.reach_id
    netcdf_extraction.extract_from_netcdf(input_nc, reach_id)
