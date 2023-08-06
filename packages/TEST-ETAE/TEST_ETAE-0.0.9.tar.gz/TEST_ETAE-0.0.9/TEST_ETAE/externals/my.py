#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :my.py
# @Time     :2021/2/8
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @File     :my.py
# @Time     :2021/2/4
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
fig = plt.figure()
fig.set(alpha=0.2)

def fittransform(inputs, cols):
    for col in cols:
        X = inputs[col]
        y = sklearn.utils.validation.column_or_1d(X, warn=True)
        label_encoder = sklearn.preprocessing.LabelEncoder.fit(list(X) + ['unknown'])
        classes = label_encoder.classes_
        y = sklearn.utils.validation.column_or_1d(y, warn=True)
        indices = np.isin(y, classes)

        y_transformed = np.searchsorted(classes, y)
        y_transformed[~indices] = -1
        inputs[col] = y_transformed
    return inputs

def timeMapper(inputs, cols, result_column, time_interval_min):
    outputs = inputs
    def colmapper(x):
        return x % (3600 * 24) // (time_interval_min * 60)
    for idx, col in enumerate(cols):
        X = outputs[col]
        mapped_col = X.apply(colmapper).values
        mapped_col_name = result_column + '_' + str(idx)
        outputs[mapped_col_name] = mapped_col
    return outputs
