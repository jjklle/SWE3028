# @Time   : 2021/03/20
# @Author : Yushuo Chen
# @Email  : chenyushuo@ruc.edu.cn

"""
save and load example
========================
Here is the sample code for the save and load in RecBole.

The path to saved data or model can be found in the output of RecBole.
"""


from recbole.quick_start import run_recbole, load_data_and_model
from recbole.utils.case_study import full_sort_topk
import torch
import numpy as np
import sys

import argparse


def load_example(user_id):
    # Filtered dataset and split dataloaders are created according to 'config'.
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file="./saved/BPR-Apr-26-2023_21-07-39.pth",
    )
    # user_ls = [i for i in range(1,2887)]
    topk_score, topk_iid_list = full_sort_topk([user_id], model, test_data, k=10, device=config['device'])
    # print(topk_score)  # scores of top 10 items
    # print(topk_iid_list)  # internal id of top 10 items
    external_item_list = dataset.id2token(dataset.iid_field, topk_iid_list.cpu())
    # print(external_item_list)  # external tokens of top 10 items
    return external_item_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_id", "-m", type=int, default=1, help="get user id")
    args, _ = parser.parse_known_args()
    recommend_ls = ' '.join(load_example(args.user_id).tolist()[0])
    f = open("recommend_ls.txt", "w")
    f.write(recommend_ls)
    f.close

