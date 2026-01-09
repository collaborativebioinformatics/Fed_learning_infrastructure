#!/bin/bash

set -eo pipefail

export DATA_PATH="../../simulated_sites"

# recode case/control as 2/1 for plink logistic regression
for site in 1 2; do
    python3 map_pheno.py \
        "${DATA_PATH}/site${site}/site${site}_pheno.pheno" \
        "${DATA_PATH}/site${site}/site${site}_pheno_recoded.pheno"
done


for site in 1 2; do
    echo "Running GWAS for site${site}..."
    export SITE="site${site}"
    plink2 --bfile ${DATA_PATH}/${SITE}/site${site}_geno \
        --glm no-firth hide-covar \
        --ci 0.95 \
        --freq \
        --pheno ${DATA_PATH}/${SITE}/site${site}_pheno_recoded.pheno \
        --pheno-name Phen1 \
        --covar ${DATA_PATH}/${SITE}/site${site}_geno.covar \
        --covar-name Sex Age \
        --out gwas_${SITE}
done
echo "GWAS analysis completed for all sites."


# merge data from .afreq files with .glm.logistic files into required format for GWAMA
for site in 1 2; do
    python3 merge_gwas_results.py \
        "gwas_site${site}.afreq" \
        "gwas_site${site}.Phen1.glm.logistic" \
        "gwas_site${site}_for_gwama.txt"
done
echo "GWAMA input files generated for all sites."
