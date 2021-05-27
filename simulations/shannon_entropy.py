import pandas as pd
import numpy as np

def intervals(first_difference):
    if first_difference <= 2:
        return "<1"
    elif 2 < first_difference <= 6:
        return "1<<2"
    elif 6 < first_difference <= 11:
        return "2<<3"
    else:
        return ">3"

def entropy(data):
    info = [p*np.log(p) for p in data.value_counts(normalize=True)]
    return -sum(info)

def sample_entropy(filename, window):
    df = pd.read_csv(filename, delimiter=";")
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"])
    df["TimeDiff"] = df["TimeStamp"].diff()
    df["TimeDiff_mili"] = df["TimeDiff"].dt.microseconds/1000
    df["Category"] = df["TimeDiff_mili"].apply(intervals)

    start = 2
    sample = df.iloc[start:start+window]    

    return entropy(sample["Category"])