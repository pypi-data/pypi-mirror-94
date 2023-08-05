#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2020 Louis Richard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so.

"""c_4_k.py
@author: Louis Richard
"""

import numpy as np

from .cross import cross
from .dot import dot


def c_4_k(r_list):
    """Calculates reciprocal vectors in barycentric coordinates.

    Parameters
    ----------
    r_list : list of xarray.DataArray
        Position of the spacecrafts.

    Returns
    -------
    k_list : list of xarray.DataArray
        Reciprocal vectors in barycentric coordinates.

    Notes
    -----
    The units of reciprocal vectors are the same as [1/r].

    """

    mms_list = np.arange(4)

    k_list = [r_list[0].copy()] * 4

    mms_lists_rolled = [np.roll(mms_list, i) for i in range(4)]

    for i, alpha, beta, gamma in zip(mms_lists_rolled):
        dr_jk_x_dr_jm = cross(r_list[beta]-r_list[alpha],
                              r_list[gamma]-r_list[alpha])

        dr12 = r_list[i]-r_list[alpha]

        k_list[i] = dr_jk_x_dr_jm / dot(dr_jk_x_dr_jm, dr12)

    return k_list
