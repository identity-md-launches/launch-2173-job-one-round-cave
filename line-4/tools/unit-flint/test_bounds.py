"""Exact inclusive bounds, invalid claims, and legacy CLI interoperability."""
import contextlib
from fractions import Fraction
import io
import json
import random
import unittest

from unit_flint import main


class BoundsTests(unittest.TestCase):
    def invoke(self, expression, *options):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main([*options, '--json', '--', expression])
        return code, json.loads(out.getvalue()) if out.getvalue() else None, err.getvalue()

    def test_transfer_time(self):
        code, result, err = self.invoke('5 MiB / (2 MiB/s)',
                                        '--at-least', '2000 ms', '--at-most', '3 s')
        self.assertEqual((code, err), (0, ''))
        self.assertEqual(result['value'], '2.5')
        self.assertEqual(result['bounds'], {
            'base_unit': 's', 'inclusive': True,
            'at_least': {'expression': '2000 ms', 'base_value': '2', 'passes': True},
            'at_most': {'expression': '3 s', 'base_value': '3', 'passes': True},
            'passes': True,
        })

    def test_inclusive_and_one_sided(self):
        for expression, flag, bound, passes in [
            ('1 m', '--at-least', '100 cm', True),
            ('1 m', '--at-most', '100 cm', True),
            ('-1 s', '--at-least', '-2 s', True),
            ('-1 s', '--at-most', '-2 s', False),
            ('0 m', '--at-least', '1 mm', False),
            ('0 m', '--at-most', '0 km', True),
            ('1 m / 3 s', '--at-most', '0.3333333333333333 m/s', False),
            ('0.1 + 0.2', '--at-least', '0.3', True),
        ]:
            with self.subTest(expression=expression, flag=flag):
                code, result, err = self.invoke(expression, flag + '=' + bound)
                self.assertEqual((code, err), (0 if passes else 1, ''))
                self.assertIs(result['bounds']['passes'], passes)

    def test_invalid_bounds_produce_no_partial_stdout(self):
        for options, message in [
            (['--at-least', '0 s'], 'bound dimension'),
            (['--at-most='], 'expected a number'),
            (['--at-most', '1/0 * m'], 'division by zero'),
            (['--at-least', '2 m', '--at-most', '100 cm'], 'lower bound exceeds'),
            (['--at-least', '(' * 40 + 'm' + ')' * 40], 'nesting'),
            (['--at-most', '(1e100)^12 * m'], 'arithmetic budget'),
            (['--at-most', '9 unknown'], 'unknown unit'),
            (['--at-most', '0'], 'bound dimension'),
        ]:
            with self.subTest(options=options):
                code, result, err = self.invoke('0 m', *options)
                self.assertEqual((code, result), (2, None))
                self.assertIn(message, err)
                self.assertNotIn('Traceback', err)

    def test_equal_endpoints_and_order_after_conversion(self):
        code, result, err = self.invoke('1 m', '--at-least', '100 cm', '--at-most', '1 m')
        self.assertEqual((code, err), (0, ''))
        self.assertTrue(result['bounds']['passes'])
        code, result, err = self.invoke('1 m', '--at-least', '1 m', '--at-most', '99 cm')
        self.assertEqual((code, result), (2, None))
        self.assertIn('lower bound exceeds', err)

    def test_expect_and_bounds_all_must_pass(self):
        for claim, upper, code in [('100 cm', '2 m', 0), ('2 m', '2 m', 1),
                                   ('100 cm', '99 cm', 1), ('2 m', '99 cm', 1)]:
            actual, result, err = self.invoke('1 m', '--expect', claim,
                                              '--at-most', upper, '--to', 'cm')
            self.assertEqual((actual, err), (code, ''))
            self.assertEqual(result['value'], '100')
            self.assertEqual(result['bounds']['base_unit'], 'm')
            self.assertEqual(result['check']['base_unit'], 'm')

    def test_plain_output(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(['1 m', '--at-least', '0 m', '--at-most', '99 cm'])
        self.assertEqual(code, 1)
        self.assertEqual(out.getvalue(), '1 m\npass: at least 0 m (inclusive)\n'
                                         'fail: at most 99 cm (inclusive)\n')

    def test_seeded_ranges_against_fraction_oracle(self):
        rng = random.Random(2404)
        for _ in range(200):
            numerator = rng.randrange(-1000, 1001)
            denominator = rng.randrange(1, 40)
            low = rng.randrange(-1000, 1001)
            high = low + rng.randrange(0, 1001)
            value = Fraction(numerator, denominator)
            passes = Fraction(low, 100) <= value <= Fraction(high, 100)
            code, result, err = self.invoke(f'{numerator}/{denominator} * m',
                                            '--at-least=' + f'{low} cm',
                                            '--at-most=' + f'{high} cm')
            self.assertEqual((code, err), (0 if passes else 1, ''))
            self.assertIs(result['bounds']['passes'], passes)


if __name__ == '__main__':
    unittest.main()
