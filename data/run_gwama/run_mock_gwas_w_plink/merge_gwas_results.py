# merge data from .afreq files with .glm.logistic files into required format for GWAMA
# 
# PLINK2 .afreq columns:
# #CHROM	ID	REF	ALT	ALT_FREQS	OBS_CT
# 1	SNP1	C	A	0.45155	20000
# 1	SNP2	C	A	0.02785	20000
# 1	SNP3	C	A	0.2027	20000
#
# PLINK2 .glm.logistic columns:
# #CHROM	POS	ID	REF	ALT	A1	TEST	OBS_CT	OR	LOG(OR)_SE	L95	U95	Z_STAT	P	ERRCODE
# 1	10000	SNP1	C	A	A	ADD	10000	0.850849	0.147546	0.637178	1.13617	-1.09471	0.273645	.
# 1	20000	SNP2	C	A	A	ADD	10000	1.21586	0.42042	0.53336	2.7717	0.464892	0.642009	.
# 1	30000	SNP3	C	A	A	ADD	10000	0.876204	0.190189	0.603554	1.27202	-0.694867	0.487139	.
#
# GWAMA input format
# 1) MARKERNAME – snp name
# 2) EA – effect allele
# 3) NEA – non effect allele
# 4) OR - odds ratio
# 5) OR_95L - lower confidence interval of OR
# 6) OR_95U - upper confidence interval of OR
# 7) BETA – beta
# 8) SE – std. error

# Usage
#!/bin/bash
# site=1
# python3 merge_gwas_results.py \
#         "gwas_site${site}.afreq" \
#         "gwas_site${site}.glm.logistic" \
#         "gwas_site${site}_for_gwama.txt"
# done

import sys
import pandas as pd
import numpy as np

df = pd.read_csv(sys.argv[1], delim_whitespace=True)
df_glm = pd.read_csv(sys.argv[2], delim_whitespace=True)
merged = pd.merge(df, df_glm, on=['#CHROM', 'ID', 'REF', 'ALT'])

# Calculate BETA as log(OR)
merged['BETA'] = np.log(merged['OR'])

# Select columns for GWAMA format
merged_gwama = merged[['ID', 'ALT', 'REF', 'OR', 'L95', 'U95', 'BETA', 'LOG(OR)_SE']]
merged_gwama.columns = ['MARKERNAME', 'EA', 'NEA', 'OR', 'OR_95L', 'OR_95U', 'BETA', 'SE']
merged_gwama.to_csv(sys.argv[3], sep="\t", index=False)
print(f"Merged GWAS results saved to {sys.argv[3]}")
