#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :mapItem.py
# @Time     :2021/2/2
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import os
import sklearn.metrics as metrics
import sklearn.linear_model as linear_model
import sklearn.preprocessing as preprocessing
import sklearn.model_selection as model_selection
import sklearn.tree as tree
import sklearn.impute as impute
import sklearn.base as base
import sklearn.ensemble as emsemble
import sklearn.neighbors as neighbors
import sklearn.svm as svm

import lightgbm as lgb
import importlib



# MAPPING = {
#     # ------------------------------------------------------- Transorm Component
#     'MinMaxScaler':MinMaxScaler,
#     'QuantileTransformer': QuantileTransformer,
#     'PowerTransformer': PowerTransformer,
#     # ------------------------------------------------------- End Transorm Component
#
#     # ------------------------------------------------------- Training Component
#     'LinearRegression': LinearRegression,
#     'Ridge': Ridge,
#     'RidgeCV': RidgeCV
#     # ------------------------------------------------------- End Training Component
# }

# TODO(jiawei.li@shopee.com): To many module need to load ?
def build_mapping_classes():
    mapping_classes = [
        metrics,
        linear_model,
        preprocessing,
        model_selection,
        tree,
        impute,
        base,
        lgb,
        emsemble,
        neighbors,
        svm,
    ]
    params = importlib.import_module('externals')
    mapping_classes.append(params)
    return mapping_classes
