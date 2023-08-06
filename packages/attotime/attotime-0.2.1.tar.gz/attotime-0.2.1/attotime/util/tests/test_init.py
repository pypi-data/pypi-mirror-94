# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest

from attotime import util
from decimal import Decimal

class TestInitFunctions(unittest.TestCase):
    def test_tuple_add(self):
        result = util.tuple_add((0,), (1,))
        self.assertEqual(result, (1,))

        result = util.tuple_add((-1,), (0,))
        self.assertEqual(result, (-1,))

        result = util.tuple_add((0, 1), (2, 3))
        self.assertEqual(result, (2, 4))

        result = util.tuple_add((0, 1), (-2, -3))
        self.assertEqual(result, (-2, -2))

    def test_decimal_stringify(self):
        result = util.decimal_stringify(Decimal(0))
        self.assertEqual(result, '0')

        result = util.decimal_stringify(Decimal(1.0))
        self.assertEqual(result, '1')

        result = util.decimal_stringify(Decimal(-1.0))
        self.assertEqual(result, '-1')

        result = util.decimal_stringify(Decimal(25))
        self.assertEqual(result, '25')

        result = util.decimal_stringify(Decimal(-25))
        self.assertEqual(result, '-25')

        result = util.decimal_stringify(Decimal('2567.8'))
        self.assertEqual(result, '2567.8')

        result = util.decimal_stringify(Decimal('-2567.8'))
        self.assertEqual(result, '-2567.8')

        result = util.decimal_stringify(Decimal(1500))
        self.assertEqual(result, '1500')

        result = util.decimal_stringify(Decimal(-1500))
        self.assertEqual(result, '-1500')

        result = util.decimal_stringify(Decimal('1E16'))
        self.assertEqual(result, '10000000000000000')

        result = util.decimal_stringify(Decimal('-1E16'))
        self.assertEqual(result, '-10000000000000000')

        result = util.decimal_stringify(Decimal('1E-16'))
        self.assertEqual(result, '0.0000000000000001')

        result = util.decimal_stringify(Decimal('-1E-16'))
        self.assertEqual(result, '-0.0000000000000001')

        result = util.decimal_stringify(Decimal('1E-9'))
        self.assertEqual(result, '0.000000001')

        result = util.decimal_stringify(Decimal('-1E-9'))
        self.assertEqual(result, '-0.000000001')
