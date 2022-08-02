#!/usr/bin/env python3
#
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import json
import numpy as np
import os
import sys

import pandas as pd

def format_melanoma_dataset(dataset_root_path):
#    train_label_set = set()
#    is_save_sample = True
    with open(os.path.join(dataset_root_path, "split.json")) as fin:
        data_splits = json.load(fin)
 
    df = pd.read_csv(dataset_root_path + "dataset/meta.csv", sep=',')
    df = df.drop(['Unnamed: 0', 'patient_id', 'diagnosis', 'target'], axis=1)
    df['sex'] = df['sex'].fillna(' ')
    df['age_approx']  = df['age_approx'].fillna(0)
    df['img'] = "dataset/" + df['image_name'].astype(str) + '.jpg'
    df['text'] = df['sex'] + '.' + + df['age_approx'].astype(str)  # + '.' + df['anatom_site_general_challenge']
    df = df.drop(['sex', 'age_approx'], axis=1) # 'anatom_site_general_challenge'], axis=1)
    df = df.rename(columns={'image_name': 'id', 'benign_malignant': 'label'})
    # df = df.dropna()
    columns = ['id', 'text', 'img', 'label']
    df = df[columns] 

    for split_name in data_splits:
        list_of_img = data_splits[split_name]
        df_obj = df[df['id'].isin(list_of_img)]
        with open(os.path.join(dataset_root_path, split_name + ".jsonl"), "w") as fw:
            # filter df to incude only images form the split_name
            for id, row in df_obj.iterrows():
                dobj = row.to_dict()
                fw.write("%s\n" % json.dumps(dobj))


if __name__ == "__main__":
    # Path to the directory for MMIMDB
    format_melanoma_dataset(sys.argv[1])
