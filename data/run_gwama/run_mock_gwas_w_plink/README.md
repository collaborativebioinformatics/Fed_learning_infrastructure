# README

This directory contains scripts and instructions to run a mock genome-wide association study (GWAS) using PLINK on simulated federated genetic data.

## Generate data

Go to the `data/simulated_sites/` directory and follow the instructions in its `README.md` file to generate synthetic genotype and phenotype data for multiple sites.

The input files assumed here by the `run_gwas.sh` script were first created using `generate_federated_sites.sh` script in `data/simulated_sites/`, sites 1 and 2 only, downscaling the number of samples and SNPs by one order of magnitude for faster testing.

## Run GWAS

Run GWAS analysis with PLINK2 (https://www.cog-genomics.org/plink/2.0/) with some minor conversion steps with Python. 
These deps can easily be installed via conda (or plain Python venv):

```{bash}
conda create -n gwas_env python=3.12 pandas
conda activate gwas_env
echo $CONDA_PREFIX
```

Download and install the `plink2` binary file for your OS from https://www.cog-genomics.org/plink/2.0/ in the `$CONDA_PREFIX/bin/` directory so that it is available in your PATH.


# run the GWAS analysis
```{bash}
cd data/run_gwama/run_mock_gwas_w_plink
bash run_gwas.sh
```

The `map_pheno.py` script is used to recode the phenotype values from 0/1 to 1/2 as required by PLINK for case/control studies.
The `merge_gwas_results.py` script merges the allele frequency data from the `.afreq` files with the logistic regression results from the `.glm.logistic` files to create input files suitable for GWAMA meta-analysis.

