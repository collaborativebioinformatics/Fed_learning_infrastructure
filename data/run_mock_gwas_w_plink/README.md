# README

This directory contains scripts and instructions to run a mock genome-wide association study (GWAS) using PLINK on simulated federated genetic data.

## Generate data

Go to the `data/simulated_sites/` directory and follow the instructions in its README to generate synthetic genotype and phenotype data for multiple sites.

The .logistic files in this directory were created using `generate_federated_sites.sh` script in `data/simulated_sites/`, sites 1 and 2 only, downscaling the number of samples and SNPs by one order of magnitude for faster testing.

## Run GWAS

```{bash}
cd data/run_mock_gwas_w_plink
bash run_gwas.sh
```

The `map_pheno.py` script is used to recode the phenotype values from 0/1 to 1/2 as required by PLINK for case/control studies.


