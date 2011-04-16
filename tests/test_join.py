#!/usr/bin/env python

import unittest

from csvkit import join

class TestJoin(unittest.TestCase):
    def setUp(self):
        self.tab1 = [
            ['id', 'name', 'i_work_here'],
            [u'1', u'Chicago Reader', u'first'],
            [u'2', u'Chicago Sun-Times', u'only'],
            [u'3', u'Chicago Tribune', u'only'],
            [u'1', u'Chicago Reader', u'second']]

        self.tab2 = [
            ['id', 'age', 'i_work_here'],
            [u'1', u'first', u'0'],
            [u'4', u'only', u'0'],
            [u'1', u'second', u'0'],
            [u'2', u'only', u'0', u'0']] # Note extra value in this column

    def test_get_join_column(self):
        self.assertEqual(join._get_join_column(self.tab1[0], 'id'), 0)

    def test_get_join_column_invalid(self):
        self.assertRaises(join.JoinError, join._get_join_column, self.tab1[0], 'no_id')

    def test_get_ordered_keys(self):
        self.assertEqual(join._get_ordered_keys(self.tab1[1:], 0), [u'1', u'2', u'3', u'1'])
        self.assertEqual(join._get_ordered_keys(self.tab2[1:], 0), [u'1', u'4', u'1', u'2'])

    def test_get_mapped_keys(self):
        self.assertEqual(join._get_mapped_keys(self.tab1[1:], 0), {
            u'1': [[u'1', u'Chicago Reader', u'first'], [u'1', u'Chicago Reader', u'second']],
            u'2': [[u'2', u'Chicago Sun-Times', u'only']],
            u'3': [[u'3', u'Chicago Tribune', u'only']]})

    def test_inner_join(self):
        self.assertEqual(join.inner_join(self.tab1, 'id', self.tab2, 'id'), [
            ['id', 'name', 'i_work_here', 'id', 'age', 'i_work_here'],
            [u'1', u'Chicago Reader', u'first', u'1', u'first', u'0'],
            [u'1', u'Chicago Reader', u'first', u'1', u'second', u'0'],
            [u'2', u'Chicago Sun-Times', u'only', u'2', u'only', u'0', u'0'],
            [u'1', u'Chicago Reader', u'second', u'1', u'first', u'0'],
            [u'1', u'Chicago Reader', u'second', u'1', u'second', u'0']])

    def test_full_outer_join(self):
        jointab = join.full_outer_join(self.tab1, 'id', self.tab2, 'id')
        self.assertEqual(len(jointab), len(self.tab1) + len(self.tab2) - 1)
        self.assertEqual(jointab.headers(), ['id', 'name', 'i_work_here', 'age', 'i_work_here_2'])
        self.assertEqual(jointab.row(0), [1, u'Chicago Reader', False, 40, False])
        self.assertEqual(jointab.row(2), [3, u'Chicago Tribune', True, None, None])
        self.assertEqual(jointab.row(3), [4, None, None, 5, False])
        self.assertEqual(jointab.count_rows(), 4)

    def test_left_outer_join(self):
        jointab = join.left_outer_join(self.tab1, 'id', self.tab2, 'id')
        self.assertEqual(len(jointab), len(self.tab1) + len(self.tab2) - 1)
        self.assertEqual(jointab.headers(), ['id', 'name', 'i_work_here', 'age', 'i_work_here_2'])
        self.assertEqual(jointab.row(0), [1, u'Chicago Reader', False, 40, False])
        self.assertEqual(jointab.row(2), [3, 'Chicago Tribune', True, None, None])
        self.assertEqual(jointab.count_rows(), 3)

    def test_right_outer_join(self):
        jointab = join.right_outer_join(self.tab1, 'id', self.tab2, 'id')
        self.assertEqual(len(jointab), len(self.tab1) + len(self.tab2) - 1)
        self.assertEqual(jointab.headers(), ['id', 'name', 'i_work_here', 'age', 'i_work_here_2'])
        self.assertEqual(jointab.row(0), [1, u'Chicago Reader', False, 40, False])
        self.assertEqual(jointab.row(2), [4, None, None, 5, False])
        self.assertEqual(jointab.count_rows(), 3)