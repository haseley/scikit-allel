# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import numpy as np
from nose.tools import eq_ as eq, assert_is_instance, assert_raises
from allel.test.tools import assert_array_equal, assert_array_nanclose


from allel.stats import ihs, xpehh, nsl, xpnsl
from allel.opt.stats import ssl01_scan_int8, nsl01_scan_int8, ihh01_scan_int8,\
    ssl2ihh


def sum_ssl(ssl, *args, **kwargs):
    return np.sum(ssl)


def test_ssl01_scan_int8_a():

    # 2 haplotypes, identical
    h = np.array([[0, 0],
                  [0, 0],
                  [0, 0]], dtype='i1')
    expect0 = [1, 2, 3]
    expect1 = [0, 0, 0]
    actual0, actual1 = ssl01_scan_int8(h, sum_ssl)
    assert_array_equal(expect0, actual0)
    assert_array_equal(expect1, actual1)


def test_ssl01_scan_int8_b():

    # 2 haplotypes, identical
    h = np.array([[1, 1],
                  [1, 1],
                  [1, 1]], dtype='i1')
    expect0 = [0, 0, 0]
    expect1 = [1, 2, 3]
    actual0, actual1 = ssl01_scan_int8(h, sum_ssl)
    assert_array_equal(expect0, actual0)
    assert_array_equal(expect1, actual1)


def test_ssl01_scan_int8_c():

    # 2 haplotypes, identical
    h = np.array([[0, 0],
                  [0, 0],
                  [1, 1],
                  [1, 1]], dtype='i1')
    expect0 = [1, 2, 0, 0]
    expect1 = [0, 0, 3, 4]
    actual0, actual1 = ssl01_scan_int8(h, sum_ssl)
    assert_array_equal(expect0, actual0)
    assert_array_equal(expect1, actual1)


def test_ssl01_scan_int8_d():

    # 2 haplotypes, different
    h = np.array([[0, 1],
                  [0, 1],
                  [1, 0],
                  [1, 0]], dtype='i1')
    expect0 = [0, 0, 0, 0]
    expect1 = [0, 0, 0, 0]
    actual0, actual1 = ssl01_scan_int8(h, sum_ssl)
    assert_array_equal(expect0, actual0)
    assert_array_equal(expect1, actual1)


def test_ssl01_scan_int8_e():

    # 3 haplotypes, 3 pairs, identical
    h = np.array([[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]], dtype='i1')
    expect0 = [3, 6, 9]
    expect1 = [0, 0, 0]
    actual0, actual1 = ssl01_scan_int8(h, sum_ssl)
    assert_array_equal(expect0, actual0)
    assert_array_equal(expect1, actual1)


def test_ssl01_scan_int8_f():

    # 4 haplotypes,
    h = np.array([[0, 0, 1, 1],
                  [0, 0, 1, 1],
                  [0, 0, 1, 1]], dtype='i1')
    expect0 = [1, 2, 3]
    expect1 = [1, 2, 3]
    actual0, actual1 = ssl01_scan_int8(h, sum_ssl)
    assert_array_equal(expect0, actual0)
    assert_array_equal(expect1, actual1)


def test_nsl01_scan_int8_a():

    h = np.array([[0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1]], dtype='i1')
    nsl0, nsl1 = nsl01_scan_int8(h)
    expect_nsl0 = [1, 2, 3, 4]
    assert_array_nanclose(expect_nsl0, nsl0)
    expect_nsl1 = [1, 2, 3, 4]
    assert_array_nanclose(expect_nsl1, nsl1)


def test_nsl01_scan_int8_b():

    h = np.array([[0, 0, 0, 1],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [1, 0, 0, 0]], dtype='i1')
    nsl0, nsl1 = nsl01_scan_int8(h)
    expect_nsl0 = [1, 4 / 3, 4 / 3, 4 / 3]
    assert_array_nanclose(expect_nsl0, nsl0)
    expect_nsl1 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_nsl1, nsl1)


def test_nsl01_scan_int8_c():

    h = np.array([[0, 0, 1],
                  [0, 1, 1],
                  [1, 1, 0],
                  [1, 0, 0]], dtype='i1')
    nsl0, nsl1 = nsl01_scan_int8(h)
    expect_nsl0 = [1, np.nan, np.nan, 1]
    assert_array_nanclose(expect_nsl0, nsl0)
    expect_nsl1 = [np.nan, 1, 1, np.nan]
    assert_array_nanclose(expect_nsl1, nsl1)


def test_ihh01_scan_int8_a():
    gaps = np.array([10, 10, 10], dtype='f8')
    h = np.array([[0, 0, 1],
                  [0, 1, 1],
                  [1, 1, 0],
                  [1, 0, 0]], dtype='i1')

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0.05)
    expect_ihh0 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh1, ihh1)

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0, include_edges=True)
    expect_ihh0 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh1, ihh1)


def test_ihh01_scan_int8_b():
    gaps = np.array([10, 10, 10], dtype='f8')
    h = np.array([[0, 0, 0, 1],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [1, 0, 0, 0]], dtype='i1')

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0.05)
    expect_ihh0 = [np.nan, np.nan, 10 * 2 / 3, 10 * 2 / 3]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh1, ihh1)

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0, include_edges=True)
    expect_ihh0 = [np.nan, 10 * 2 / 3, 10 * 2 / 3, 10 * 2 / 3]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh1, ihh1)


def test_ihh01_scan_int8_c():
    gaps = np.array([10, 10, 10], dtype='f8')
    h = np.array([[0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1],
                  [0, 0, 0, 1, 1, 1]], dtype='i1')

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0.05)
    expect_ihh0 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, np.nan, np.nan, np.nan]
    assert_array_nanclose(expect_ihh1, ihh1)

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0, include_edges=True)
    expect_ihh0 = [np.nan, 10, 20, 30]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, 10, 20, 30]
    assert_array_nanclose(expect_ihh1, ihh1)


def test_ihh01_scan_int8_d():
    gaps = np.array([10, 10, 10], dtype='f8')
    h = np.array([[0, 0, 1, 1, 1, 0],
                  [0, 1, 0, 1, 0, 1],
                  [1, 0, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1]], dtype='i1')

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0.05)
    expect_ihh0 = [np.nan, np.nan, 10 * 2 / 3, 10 * 2 / 3]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, np.nan, 10 * 2 / 3, 10 * 2 / 3]
    assert_array_nanclose(expect_ihh1, ihh1)

    ihh0, ihh1 = ihh01_scan_int8(h, gaps, min_ehh=0, include_edges=True)
    expect_ihh0 = [np.nan, 10 * 2 / 3, 10 * 2 / 3, 10 * 2 / 3]
    assert_array_nanclose(expect_ihh0, ihh0)
    expect_ihh1 = [np.nan, 10 * 2 / 3, 10 * 2 / 3, 10 * 2 / 3]
    assert_array_nanclose(expect_ihh1, ihh1)


def test_ssl2ihh_a():

    # 2 haplotypes, 1 pair
    ssl = np.array([3], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0
    expect = (4 * (1 + 1) / 2) + (2 * (1 + 1) / 2)
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh)
    eq(expect, actual)


def test_ssl2ihh_b():

    # 3 haplotypes, 3 pairs
    ssl = np.array([3, 0, 0], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0
    expect = (4 * (1/3 + 1/3) / 2) + (2 * (1/3 + 1/3) / 2)
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh)
    eq(expect, actual)


def test_ssl2ihh_c():

    # 3 haplotypes, 3 pairs
    ssl = np.array([3, 2, 1], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0
    expect = (4 * (1 + 2/3) / 2) + (2 * (2/3 + 1/3) / 2)
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh)
    eq(expect, actual)


def test_ssl2ihh_d():

    # 3 haplotypes, 3 pairs
    ssl = np.array([0, 1, 3], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0
    expect = (4 * (2/3 + 1/3) / 2) + (2 * (1/3 + 1/3) / 2)
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh)
    eq(expect, actual)


def test_ssl2ihh_e():

    # 2 haplotypes, 1 pair
    # no matches beyond current variant
    ssl = np.array([1], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh)
    assert np.isnan(actual), actual


def test_ssl2ihh_f():

    # 2 haplotypes, 1 pair
    # never falls to min_ehh
    ssl = np.array([4], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh)
    assert np.isnan(actual), actual


def test_ssl2ihh_g():

    # 2 haplotypes, 1 pair
    # never falls to min_ehh, but include_edges
    ssl = np.array([4], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0
    expect = (4 + 2 + 1)
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh, include_edges=True)
    eq(expect, actual)


def test_ssl2ihh_h():

    # 3 haplotypes, 3 pairs
    ssl = np.array([0, 1, 3], dtype='i4')
    gaps = np.array([1, 2, 4], dtype='f8')
    vidx = 3
    min_ehh = 0.5
    actual = ssl2ihh(ssl, max(ssl), vidx, gaps, min_ehh)
    assert np.isnan(actual), actual


def test_ihs():
    n_variants = 1000
    n_haplotypes = 20
    h = np.random.randint(0, 2, size=(n_variants, n_haplotypes),
                          dtype='i1')
    pos = np.arange(0, n_variants * 10, 10)

    for use_threads in True, False:
        for min_ehh in 0, 0.05, 0.5:
            for include_edges in True, False:
                score = ihs(h, pos, min_ehh=min_ehh,
                            include_edges=include_edges,
                            use_threads=use_threads)
                assert_is_instance(score, np.ndarray)
                eq((n_variants,), score.shape)
                eq(np.dtype('f8'), score.dtype)

    with assert_raises(ValueError):
        ihs(h, pos[1:])

    with assert_raises(ValueError):
        ihs(h, pos, map_pos=pos[1:])


def test_xpehh():
    n_variants = 1000
    n_haplotypes = 20
    h1 = np.random.randint(0, 2, size=(n_variants, n_haplotypes),
                           dtype='i1')
    h2 = np.random.randint(0, 2, size=(n_variants, n_haplotypes),
                           dtype='i1')
    pos = np.arange(0, n_variants * 10, 10)

    for use_threads in True, False:
        for min_ehh in 0, 0.05, 0.5:
            for include_edges in True, False:
                score = xpehh(h1, h2, pos, min_ehh=min_ehh,
                              include_edges=include_edges,
                              use_threads=use_threads)
                assert_is_instance(score, np.ndarray)
                eq((n_variants,), score.shape)
                eq(np.dtype('f8'), score.dtype)

    with assert_raises(ValueError):
        xpehh(h1, h2[1:], pos)

    with assert_raises(ValueError):
        xpehh(h1[1:], h2, pos)

    with assert_raises(ValueError):
        xpehh(h1, h2, pos[1:])

    with assert_raises(ValueError):
        xpehh(h1, h2, pos, map_pos=pos[1:])


def test_nsl():
    n_variants = 1000
    n_haplotypes = 20
    h = np.random.randint(0, 2, size=(n_variants, n_haplotypes),
                          dtype='i1')

    for use_threads in True, False:
        score = nsl(h, use_threads=use_threads)
        assert_is_instance(score, np.ndarray)
        eq((n_variants,), score.shape)
        eq(np.dtype('f8'), score.dtype)


def test_xpnsl():
    n_variants = 1000
    n_haplotypes = 20
    h1 = np.random.randint(0, 2, size=(n_variants, n_haplotypes),
                           dtype='i1')
    h2 = np.random.randint(0, 2, size=(n_variants, n_haplotypes),
                           dtype='i1')

    for use_threads in True, False:
        score = xpnsl(h1, h2, use_threads=use_threads)
        assert_is_instance(score, np.ndarray)
        eq((n_variants,), score.shape)
        eq(np.dtype('f8'), score.dtype)
