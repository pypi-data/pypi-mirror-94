#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :mapping.py
# @Time     :2021/1/26
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None
import os

import importlib
from ETAES.globals.mapItem import MAPPING_CLASS, MAPPING_COMPONENTS

def build_mapping(modules):
    mapping_dict = {}
    for module in modules:
        all = module.__all__
        for item in all:
            mapping_dict[item] = getattr(module, item)
    return mapping_dict

def mapping(func_name, mapping_classes = MAPPING_CLASS):
    mapping_dict = build_mapping(mapping_classes)
    return mapping_dict[func_name]

def mapping_component(name):
    return MAPPING_COMPONENTS[name]
