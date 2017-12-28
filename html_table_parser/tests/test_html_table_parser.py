import unittest
import os

__author__ = 'oswaldjones'


class TestHtmlTableParser(unittest.TestCase):

    def test_html_table_parser(self):

        from bs4 import BeautifulSoup as bs
        from html_table_parser import parser_functions as parse

        soup = bs(mock_html_table(), "html.parser")
        test_table = soup.find('table')

        twod = parse.make2d(test_table)

        # two_col_data function is case insensitive
        self.assertEqual(parse.twod_col_data(twod, 'first name'), ['Eve', 'John', 'Adam', 'Jill'])
        # last name for first row is Eve because of colspan
        self.assertEqual(parse.twod_col_data(twod, 'lAst naMe'), ['Eve', 'Doe', 'Johnson', 'Smith'])
        # points for last row is 67 because of rowspan
        self.assertEqual(parse.twod_col_data(twod, 'POINTS'), ['94', '80', '67', '67'])


def mock_html_table():
    # html table with row and colspan
    return """
    <table class="w3-table-all" style="width:100%">
        <tbody>
            <tr>
                <th>Number</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Points</th>
            </tr>
            <tr>
                <td>1</td>
                <td colspan="2">Eve</td>
                <!-- copied "Eve" from colspan -->
                <td>94</td>
            </tr>
            <tr>
                <td>2</td>
                <td>John</td>
                <td>Doe</td>
                <td>80</td>
            </tr>
            <tr>
                <td>3</td>
                <td>Adam</td>
                <td>Johnson</td>
                <td rowspan="2">67</td>
            </tr>
            <tr>
                <td>4</td>
                <td>Jill</td>
                <td>Smith</td>
                <!-- copied "67" from rowspan -->
            </tr>
        </tbody>
    </table>
    """
