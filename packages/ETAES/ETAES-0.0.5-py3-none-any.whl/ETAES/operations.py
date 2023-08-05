#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :operations.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import os

import ETAES.components as com
from ETAES.components import *
from ETAES.pipeline import Pipeline
from ETAES.utils.builder import build_config, build_paths
from ETAES import TASK_ID
from ETAES.utils.mapping import mapping_component
from ETAES.globals.mapItem import MAPPING_COMPONENTS


def build_configurations(config_path):
    kwargs = build_config(config_path)
    build_paths(task_id=TASK_ID, configs=kwargs)
    return kwargs


def excute_pipeline(config_path):
    kwargs = build_config(config_path)
    basic_cfg = kwargs['basic']
    init_item = os.path.join(basic_cfg['paths']['file_path'], basic_cfg['names']['file_name'])
    components = [
        ExampleGen,
        StatisticsGen,
        SchemaGen,
        ExampleValidator,
        Transform,
        Trainer,
        Evaluator,
        Pusher,
        Predictor
    ]
    pipeline = Pipeline(components, kwargs, init_item)
    pipeline.excute()

