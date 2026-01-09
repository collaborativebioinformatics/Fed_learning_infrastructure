#!/usr/bin/env python3
# convert REGENIE GWAS output to GWAMA input format
# 
# Regenie .regenie columns:
# CHROM GENPOS ID ALLELE0 ALLELE1 A1FREQ N TEST BETA SE CHISQ LOG10P EXTRA
# 1 10000 SNP1 C A 0.4501 100000 ADD -0.018981 0.0472442 0.161414 0.162501 NA
# 1 20000 SNP2 C A 0.440625 100000 ADD 0.0996214 0.0468343 4.49455 1.46848 NA
# 1 30000 SNP3 C A 0.183125 100000 ADD 0.0166974 0.0606897 0.0756956 0.106118 NA
#
# GWAMA output format (defaults to OR format)
# 1) MARKERNAME – snp name
# 2) EA – effect allele
# 3) NEA – non effect allele
# 4) OR - odds ratio
# 5) OR_95L - lower confidence interval of OR
# 6) OR_95U - upper confidence interval of OR
# 7) BETA – beta
# 8) SE – std. error
# 
# Usage:
# python3 regenie_to_gwama.py <input.regenie> <output_gwama.txt> <mode>
# where <mode> is 'or' for odds ratio (binary trait) or 'qt' for quantitative trait

import argparse
import pandas as pd
import numpy as np
from scipy.stats import norm


def parse_args():
    parser = argparse.ArgumentParser(description="Convert REGENIE GWAS output to GWAMA input format.")
    parser.add_argument("input", help="Path to .regenie output file")
    parser.add_argument("output", help="Path to write GWAMA-formatted output")
    parser.add_argument("mode", choices=["or", "qt"], help="Use 'or' for binary trait (odds ratios) or 'qt' for quantitative trait")
    return parser.parse_args()


def main():
    args = parse_args()

    gwas = pd.read_csv(args.input, sep="\s+")
    if args.mode == 'or':
        z_score = norm.ppf(0.975) # 97.5 percentile
        gwas['OR'] = np.exp(gwas['BETA'])
        gwas['OR_95L'] = np.exp(gwas['BETA'] - z_score * gwas['SE'])
        gwas['OR_95U'] = np.exp(gwas['BETA'] + z_score * gwas['SE'])

        gwas.rename(columns={'ID': 'MARKERNAME', 'ALLELE1': 'EA', 'ALLELE0': 'NEA'}, inplace=True)
        gwas[['MARKERNAME', 'EA', 'NEA', 'OR', 'OR_95L', 'OR_95U', 'BETA', 'SE']].to_csv(args.output, sep="\t", index=False)
    else:
        gwas.rename(columns={'ID': 'MARKERNAME', 'ALLELE1': 'EA', 'ALLELE0': 'NEA'}, inplace=True)
        gwas[['MARKERNAME', 'EA', 'NEA', 'BETA', 'SE']].to_csv(args.output, sep="\t", index=False)

if __name__ == "__main__":
    main()
