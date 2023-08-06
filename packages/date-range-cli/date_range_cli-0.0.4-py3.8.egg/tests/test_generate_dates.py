import pendulum

import pytest
from unittest.mock import MagicMock

from date_range.generate_dates import generate_dates, generate_date_range_and_output

start_date = pendulum.date(2019, 1, 10)
end_date = pendulum.date(2019, 1, 13)


def test_generate_date_range_ascending():
    date_list = list(generate_dates(start_date, end_date, 'asc'))
    expected_date_list = [
        pendulum.date(2019, 1, 10),
        pendulum.date(2019, 1, 11),
        pendulum.date(2019, 1, 12),
        pendulum.date(2019, 1, 13)
    ]
    assert date_list == expected_date_list


def test_generate_date_range_descending():
    date_list = list(generate_dates(start_date, end_date, 'desc'))
    expected_date_list = [
        pendulum.date(2019, 1, 13),
        pendulum.date(2019, 1, 12),
        pendulum.date(2019, 1, 11),
        pendulum.date(2019, 1, 10)
    ]
    assert date_list == expected_date_list


def test_generate_date_range_same_date():
    date_list = list(generate_dates(start_date, start_date, 'asc'))
    expected_date_list = [
        pendulum.date(2019, 1, 10)
    ]
    assert date_list == expected_date_list


def test_generate_date_range_invalid_date_range():
    with pytest.raises(ValueError, match='invalid date range start date is after end date.'):
        for date in generate_dates(end_date, start_date, 'asc'):
            print(date)


def test_print_to_screen(capsys):
    args = MagicMock()
    args.start_date = start_date
    args.end_date = end_date
    args.sort_order = 'asc'
    args.output_format = None

    generate_date_range_and_output(args)
    printed_ouptut = capsys.readouterr().out
    expected_output = '2019-01-10 2019-01-11 2019-01-12 2019-01-13 '
    assert printed_ouptut == expected_output


def test_print_to_screen_with_formatting(capsys):
    args = MagicMock()
    args.start_date = start_date
    args.end_date = end_date
    args.sort_order = 'asc'
    args.output_format = '%m_%d_%Y'

    generate_date_range_and_output(args)
    printed_ouptut = capsys.readouterr().out
    expected_output = '01_10_2019 01_11_2019 01_12_2019 01_13_2019 '
    assert printed_ouptut == expected_output

