#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :main.py
# @Time     :2021/2/7
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None


# from TEST_ETAE.main import infer
import pandas as pd
import json
import sys
from ETAES.operations import excute_pipeline, build_pipeline, build_configurations

#
# config_path = 'TEST_ETAE/cfgs/config.yaml'
# waybills_df = pd.read_csv('TEST_ETAE/data/waybills.csv')
# waybills_df.drop(['Unnamed: 0', 'delivery_time'], axis=1, inplace=True)
# waybills_str = waybills_df[:3].to_json(orient="records")
# inputs = json.loads(waybills_str)
# kwargs = build_configurations(config_path)
# kwargs['basic']['task_id'] = '1612750425'

def init(kwargs, inputs):
    return build_pipeline(kwargs, inputs)

# TODO: 将infer和init区分开
def infer(kwargs, inputs):
    pipeline = init(kwargs, inputs)
    return excute_pipeline(pipeline)

# infer()
# if __name__ == '__main__':
#     waybills_df = pd.read_csv('TEST_ETAE/data/waybills.csv')
#     waybills_df.drop(['Unnamed: 0', 'delivery_time'], axis=1, inplace=True)
#     waybills_str = waybills_df[:3].to_json(orient="records")
#     waybills_js = json.loads(waybills_str)
#
#     # def find_config_from_taskid(task_id):
#     #     config_path = 'cfgs/config.yaml'
#     #     return build_configurations(config_path)
#     #
#     # task_id = '1612691303'
#     # kwargs = find_config_from_taskid(task_id)
#     # kwargs['basic']['task_id'] = task_id
#     #
#     # result = infer(kwargs, waybills_js)
#     # print(result)
#
#     _, config_path = sys.argv
#     kwargs = build_configurations(config_path)
#     if kwargs['basic']['status'] == 'online':
#         kwargs['basic']['task_id'] = '1612750425'
#         waybills_df = pd.read_csv('TEST_ETAE/data/waybills.csv')
#         waybills_df.drop(['Unnamed: 0'], axis=1, inplace=True)
#         waybills_str = waybills_df[:2].to_json(orient="records")
#         waybills_js = json.loads(waybills_str)
#         excute_pipeline(kwargs, waybills_js)
#     else:
#         excute_pipeline(kwargs, js=None)