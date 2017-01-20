#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from numpy import linspace, isnan
from numpy.testing import assert_equal
from pandas import DataFrame, Series
from json_tricks import dumps, loads


COLUMNS = OrderedDict((
	('name', ('Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliett',)),
	('count', linspace(0, 10, 10, dtype=int)),
	('real', linspace(0, 7.5, 10, dtype=float)),
	('special', (float('NaN'), float('+inf'), float('-inf'), float('+0'), float('-0'), 1, 2, 3, 4, 5)),
	#todo: other types?
))


def test_pandas_dataframe():
	df = DataFrame(COLUMNS, columns=tuple(COLUMNS.keys()))
	txt = dumps(df, allow_nan=True)
	back = loads(txt)
	assert isnan(back.ix[0, -1])
	assert (df.equals(back))
	assert (df.dtypes == back.dtypes).all()
	df = DataFrame(COLUMNS, columns=tuple(COLUMNS.keys()))
	txt = dumps(df, primitives=True, allow_nan=True)
	back = loads(txt)
	assert isinstance(back, dict)
	assert isnan(back['special'][0])
	assert all(df.index.values == tuple(back.pop('index')))
	for name, col in back.items():
		assert name in COLUMNS
		assert_equal(list(COLUMNS[name]), col)


def test_pandas_series():
	for name, col in COLUMNS.items():
		ds = Series(data=col, name=name)
		txt = dumps(ds, allow_nan=True)
		back = loads(txt)
		assert (ds.equals(back))
		assert ds.dtype == back.dtype
	for name, col in COLUMNS.items():
		ds = Series(data=col, name=name)
		txt = dumps(ds, primitives=True, allow_nan=True)
		back = loads(txt)
		assert isinstance(back, dict)
		assert_equal(ds.index.values, back['index'])
		assert_equal(ds.values, back['data'])


