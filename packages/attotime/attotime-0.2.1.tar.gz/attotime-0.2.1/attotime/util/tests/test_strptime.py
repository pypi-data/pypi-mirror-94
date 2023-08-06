# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import calendar
import time
import unittest

from attotime.util import strptime
from attotime.tests.compat import mock

class TestStrptimeFunctions(unittest.TestCase):
    def test_get_format_fields(self):
        self.assertEqual(strptime.get_format_fields('%a%A%w%d%b%B%m%y%Y%H%I%p%M%S%f%z%Z%j%U%W%c%x%X%%'), ['%a', '%A', '%w', '%d', '%b', '%B', '%m', '%y', '%Y', '%H', '%I', '%p', '%M', '%S', '%f', '%z', '%Z', '%j', '%U', '%W', '%c', '%x', '%X', '%%'])
        self.assertEqual(strptime.get_format_fields('%o%q%v'), ['%o', '%q', '%v'])
        self.assertEqual(strptime.get_format_fields('abcd'), ['abcd'])
        self.assertEqual(strptime.get_format_fields('%a abcd %X'), ['%a', ' abcd ', '%X'])

        self.assertEqual(strptime.get_format_fields(''), [])

    def test_expand_format_fields(self):
        self.assertEqual(strptime.expand_format_fields(['%a', '%A', '%w', '%d', '%b', '%B', '%m', '%y', '%Y', '%H', '%I', '%p', '%M', '%S', '%f', '%z', '%Z', '%j', '%U', '%W', '%%']), ['%a', '%A', '%w', '%d', '%b', '%B', '%m', '%y', '%Y', '%H', '%I', '%p', '%M', '%S', '%f', '%z', '%Z', '%j', '%U', '%W', '%%'])
        self.assertEqual(strptime.expand_format_fields(['%o', '%q', '%v']), ['%o', '%q', '%v'])

        #Expansions are locale specific, so we have to mock strftime which is used to determine expansions, calendar also calls time.strftime, requiring additional mocking
        def _mock_strftime(format, timetuple):
            if timetuple == time.struct_time((1999, 3, 17, 22, 44, 55, 2, 76, 0)):
                if format == '%p':
                    return 'PM'
                elif format == '%c':
                    return 'Wed Mar 17 22:44:55 1999'
                elif format == '%x':
                    return '03/17/99'
                elif format == '%X':
                    return '22:44:55'
            elif timetuple == time.struct_time((1999, 1, 3, 1, 1, 1, 6, 3, 0)):
                if format == '%c':
                    return 'Sun Jan  3 01:01:01 1999'
                elif format == '%x':
                    return '01/03/99'
                elif format == '%X':
                    return '01:01:01'

        with mock.patch.object(calendar, 'day_abbr', new_callable=mock.PropertyMock(return_value=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])):
            with mock.patch.object(calendar, 'day_name', new_callable=mock.PropertyMock(return_value=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])) as mockDayNames:
                with mock.patch.object(calendar, 'month_abbr', new_callable=mock.PropertyMock(return_value=['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])):
                    with mock.patch.object(calendar, 'month_name', new_callable=mock.PropertyMock(return_value=['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])):
                        with mock.patch.object(time, 'strftime', side_effect=_mock_strftime):
                            self.assertEqual(strptime.expand_format_fields(['%c']), ['%a', ' ', '%b', ' ', '%d', ' ', '%H', ':', '%M', ':', '%S', ' ', '%Y'])
                            self.assertEqual(strptime.expand_format_fields(['%x']), ['%m', '/', '%d', '/', '%y'])
                            self.assertEqual(strptime.expand_format_fields(['%X']), ['%H', ':', '%M', ':', '%S'])
                            self.assertEqual(strptime.expand_format_fields(['%c', ' ', '%o', '%q', '%v']), ['%a', ' ', '%b', ' ', '%d', ' ', '%H', ':', '%M', ':', '%S', ' ', '%Y', ' ', '%o', '%q', '%v'])

    def test_get_field_size(self):
        self.assertEqual(strptime.get_field_size('2001', ['2001'], 0, 1), 4)
        self.assertEqual(strptime.get_field_size('abcd2001', ['2001'], 0, 7), 4)
        self.assertEqual(strptime.get_field_size('abcd2001', ['2001'], 0, 5), 4)

        self.assertEqual(strptime.get_field_size('abcd2001', ['BC'], 0, 7), 2)
        self.assertEqual(strptime.get_field_size('abcd2001', ['BC'], 0, 2), 2)

        self.assertEqual(strptime.get_field_size('2001', ['a', 'b', 'c', 'd'], 0, 2), -1)
        self.assertEqual(strptime.get_field_size('2001', ['2001'], 1, 2), -1)
