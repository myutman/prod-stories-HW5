import os
import pandas as pd
import numpy as np
import json

import torch


def get_markedup_uuids():
    uuids = [x[:-5] for x in os.listdir("histograms") if x != ".ipynb_checkpoints"]
    return uuids


def fix_obj_name(x):
    if type(x) is str:
        x = x.split('.')[0]
    return x


def get_data_by_ids(df, ids):
    subdf = df.loc[ids]

    hists = []
    for uuid in subdf.index:
        with open(os.path.join('histograms', uuid + '.json'), 'r') as inf:
            data = json.load(inf)
        hist = torch.cat([
            torch.FloatTensor(data["histogram_data"][8]["data"]),
            torch.FloatTensor(data["histogram_data"][9]["data"]),
            torch.FloatTensor(data["histogram_data"][10]["data"]),
            torch.FloatTensor(data["histogram_data"][11]["data"]),
        ])
        hists.append(hist)

    subdf["hist"] = hists
    subdf = subdf.applymap(fix_obj_name)
    return subdf


def convert_tensors(data):
    if (type(data) is str) and data[:len("tensor([")] == "tensor([":
        data = ' '.join(data[len("tensor(["):][:-2].split())
        data = torch.FloatTensor([float(token) for token in data.split(', ')])
    return data


def load_data_from_tsv(filename):
    df = pd.read_csv(filename, sep="\t")
    df = df.applymap(convert_tensors)
    return df