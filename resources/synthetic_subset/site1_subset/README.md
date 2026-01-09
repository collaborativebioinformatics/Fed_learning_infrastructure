# site1 synthetic dataset (GWAS-ready)

This folder contains a **single synthetic biobank/site** generated for
Phase 1 testing of the federated learning GWAS infrastructure.

## Contents

### Genotype data (PLINK format)
- `site1_geno.bed`
- `site1_geno.bim`
- `site1_geno.fam`

LD-aware synthetic genotypes generated using Doug Speed–style simulations.

### Phenotype data
- `site1_pheno.liab`  
  Continuous liability-scale phenotype
- `site1_pheno.breed`, `site1_pheno.effects`  
  Simulation metadata

### Covariates
- `site1_geno.covar`  
  Includes:
  - Sex
  - Age

## GWAS analysis (validated)

This dataset has been validated by running:

- **REGENIE v4.1**
- Binary trait (case/control derived from liability)
- Logistic regression (`--bt`)
- Covariates: Sex, Age
- Step 2 only (`--ignore-pred`)

### Derived output (not committed)
A GWAMA-compatible summary statistics file was generated externally:

- Format:
