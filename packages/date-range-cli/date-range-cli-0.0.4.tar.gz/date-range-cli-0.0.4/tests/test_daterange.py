import pendulum
import pytest

from date_range.daterange import parse_args

start_date = pendulum.date(2019, 1, 10)
end_date = pendulum.date(2019, 1, 13)


def test_no_args():
    with pytest.raises(SystemExit):
        parse_args(args=[])


def test_date_output_format():
    args = parse_args(args=[
        '-s', '2019-01-10',
        '-f', '%d_%m_%Y'
    ])
    assert args.start_date == start_date
    assert args.end_date == pendulum.now().date()
    assert args.sort_order == 'asc'
    assert args.output_format == '%d_%m_%Y'


def test_date_output_format_not_specified():
    args = parse_args(args=[
        '-s', '2019-01-10'
    ])
    assert args.start_date == start_date
    assert args.end_date == pendulum.now().date()
    assert args.sort_order == 'asc'
    assert args.output_format is None


def test_start_date_only():
    args = parse_args(args=[
        '-s', '2019-01-10'
    ])
    assert args.start_date == start_date
    assert args.end_date == pendulum.now().date()
    assert args.sort_order == 'asc'


def test_end_date_only():
    with pytest.raises(SystemExit):
        parse_args(args=[
            '-e', '2019-01-13'
        ])


def test_start_end_date_only():
    args = parse_args(args=[
        '-s', '2019-01-10',
        '-e', '2019-01-13'
    ])
    assert args.start_date == start_date
    assert args.end_date == end_date
    assert args.sort_order == 'asc'


def test_start_end_date_invalid_date():
    with pytest.raises(SystemExit):
        parse_args(args=[
            '-s', '2019-01- 10 Tx',
            '-e', '2019-01- 11 tx'
        ])


def test_start_end_date_invalid_sort_order():
    with pytest.raises(SystemExit):
        parse_args(args=[
            '-s', '2019-01-10',
            '-e', '2019-01-11',
            '-o', 'other'
        ])


def test_start_end_date_with_sort_order():
    args = parse_args(args=[
        '-s', '2019-01-10',
        '-e', '2019-01-13',
        '-o', 'desc'
    ])
    assert args.start_date == start_date
    assert args.end_date == end_date
    assert args.sort_order == 'desc'
