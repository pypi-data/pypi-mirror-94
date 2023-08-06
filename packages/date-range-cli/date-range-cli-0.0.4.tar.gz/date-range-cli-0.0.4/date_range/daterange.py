import argparse

import pendulum

from date_range.generate_dates import generate_date_range_and_output


def parse_args(args=None):
    date_parser = lambda dt: pendulum.parse(dt).date()
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-date', required=True, type=date_parser)
    parser.add_argument('-e', '--end-date', type=date_parser)
    parser.add_argument('-o', '--sort-order', choices=['asc', 'desc'], default='asc')
    parser.add_argument('-f', '--output-format', type=str)

    args = parser.parse_args(args=args)
    if args.end_date is None:
        args.end_date = pendulum.now().date()

    return args


def main():
    args = parse_args()
    generate_date_range_and_output(args)
