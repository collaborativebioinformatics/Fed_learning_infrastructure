#!/bin/bash

set -eo pipefail

export DATA_PATH="../simulated_sites"

# recode case/control as 2/1 for plink logistic regression
for site in 1 2; do
    python3 map_pheno.py \
        "${DATA_PATH}/site${site}/site${site}_pheno.pheno" \
        "${DATA_PATH}/site${site}/site${site}_pheno_recoded.pheno"
done


for site in 1 2; do
    echo "Running GWAS for site${site}..."
    export SITE="site${site}"
    plink --bfile ${DATA_PATH}/${SITE}/site${site}_geno \
        --logistic \
        --pheno ${DATA_PATH}/${SITE}/site${site}_pheno_recoded.pheno \
        --pheno-name Phen1 \
        --all-pheno \
        --covar ${DATA_PATH}/${SITE}/site${site}_geno.covar \
        --covar-name Sex \
        --out gwas_${SITE}
done
echo "GWAS analysis completed for all sites."

