#!/usr/bin/env python3
import sys
import pandas as pd

df = pd.read_csv(sys.argv[1], sep="\s+")
df["Phen1"] = df["Phen1"].map({0: "1", 1: "2"})
print(df.head())
df.to_csv(sys.argv[2], sep="\t", index=False)
