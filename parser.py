import json
import wget
import ssl
import pandas as pd
import os
import re
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

datadir = "raw_data/dress"

def main():
    file_list = os.listdir(datadir)
    file_list.sort()
    feature_list = list(set([re.search(r'(.*)[0-9]+.json', file_name).group(1) for file_name in file_list]))
    feature_list.append("ID")
    feature_list.sort()
    df = pd.DataFrame(columns=feature_list)

    for file_name in file_list:
        label = re.search(r'(.*)[0-9]+.json', file_name).group(1)
        df_slice = pd.DataFrame(columns=feature_list)

        json_file = open(os.path.join(datadir, file_name)).read()
        data = json.loads(json_file)["results"]
        product_id = [d["custom_data"]["ProductID"] for d in data]
        df_slice["ID"] = product_id
        df_slice.loc[:, "%s" % label] = 1
        df = pd.concat([df, df_slice], axis=0)

    df = df.set_index("ID")
    df = df.groupby(df.index).sum()

    for feature in feature_list:
        if feature != "ID":
            df["%s" % feature] = df["%s" % feature] > 0
    df = df.astype(int)

    df.to_csv("dress.csv")


if __name__ == "__main__":
    main()
