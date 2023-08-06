#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @File     :main.py
# @Time     :2021/2/1
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import sys
import pandas as pd
import json

from ETAES.operations import excute_pipeline, build_configurations

# Press the green button in the gutter to run the script.

# waybills_df = pd.read_csv('data/waybills.csv')
# waybills_df.drop(['Unnamed: 0', 'delivery_time'], axis=1, inplace=True)
# waybills_str = waybills_df[:2].to_json(orient="records")
# waybills_js = json.loads(waybills_str)

def find_config_from_taskid(task_id):
    config_path = 'cfgs/config.yaml'
    return build_configurations(config_path)

# task_id = '1612686172'
# kwargs = find_config_from_taskid(task_id)
# kwargs['basic']['task_id'] = task_id

def infer(kwargs, inputs):
    # kwargs = find_config_from_taskid(task_id)
    # kwargs['basic']['task_id'] = task_id
    result = excute_pipeline(kwargs, inputs)
    return result


# if __name__ == '__main__':
    # _, config_path = sys.argv
    # kwargs = build_configurations(config_path)
    # if kwargs['basic']['status'] == 'online':
    #     kwargs['basic']['task_id'] = '1612682787'
    #     waybills_df = pd.read_csv('data/waybills.csv')
    #     waybills_df.drop(['Unnamed: 0'], axis=1, inplace=True)
    #     waybills_str = waybills_df[:2].to_json(orient="records")
    #     waybills_js = json.loads(waybills_str)
    #     excute_pipeline(kwargs, waybills_js)
    # else:
    #     excute_pipeline(kwargs, js=None)
    # result = infer()
    # print(result)