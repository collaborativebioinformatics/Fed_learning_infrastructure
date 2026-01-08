# Fed_learning_infrastructure
Federated Learning (FL) Infrastructure &amp; Synthetic Data

<img src="./resources/Fed_learning_infrastructure_logo.png" alt="Federated learning infrastructure logo" width="300" height="300">

## Contributors
1. Holger Roth
2. Pravesh Parekh
3. Srikant Sarangi
4. Enamul Shimul
5. Espen Hagen
6. Mariona Jaramillo Civill
7. Ioannis Christofilogiannis
8. Konstantinos Koukoutegos

## Introduction
Large-scale genomic studies increasingly rely on multi-site collaboration to achieve sufficient statistical power for complex disease analysis. However, sharing individual-level genomic data across institutions is often constrained by privacy regulations, ethical considerations, and governance policies. Federated learning (FL) offers a promising paradigm to address these challenges by enabling collaborative model training without centralizing raw data. This project aims to design and evaluate an end-to-end federated learning framework for genome-wide association–style analyses using realistically simulated genotype and phenotype data. Synthetic genomic datasets are generated to closely resemble real-world data properties, including linkage disequilibrium (LD) structure, per-site variability, covariates, and site-level data imbalance. On top of this synthetic data layer, a federated learning infrastructure is deployed using an FL server–client architecture using NVFlare on AWS. Multiple client sites represent independent data holders with heterogeneous sample sizes and phenotype distributions, while our learning task is focused on binary phenotype prediction (Parkinson’s disease case/control status) using a logistic regression predictor.

## Goals
The goal of this project is to establish a realistic and extensible experimental framework for federated learning in genomics by combining synthetic data generation, scalable infrastructure, and privacy-aware modeling. Specifically, we aim to generate biologically plausible synthetic genotype and phenotype data with preserved LD structure, standardized genome builds, and meaningful covariates, while enabling per-site heterogeneity that mirrors real-world cohort imbalance. In parallel, we seek to deploy and evaluate a federated learning system using NVFlare on cloud infrastructure, supporting multiple client sites, containerized workflows, and continuous monitoring and validation. Within this framework, we aim to implement a state-of-the-art genotype–phenotype statistical model trained directly from PLINK-formatted data, using a custom federated training aggregator strategy, and quantify the framework's performance, robustness, and scalability. 

## Methods
1. Explain the synthetic data generation process
We generated realistic synthetic dataset for 10 different sites using the LDAK software [https://dougspeed.com/downloads/]. Specifically, the simulated phenotype was a case-control phenotype representing the case status of having Parkinson's Disease with a realistic population prevalence rate of 1%, single nucleotide polymorphism (SNP) heritability of 0.25 (on a liability scale), 20 causal SNPs per site, and using the "LDAK-Thin" effect size model with a power of -0.25. For each site, the covariates included age and sex that overall explained ~10% of the phenotypic variance. For the genotype simulation., we allowed the number of SNPs to vary between ~450,000 to ~520,000 variants per site while the sample size per site varied between 88,000 and 110,000. This resulted in synthetic data across 10 sites with varied number of subjects, slightly different number of genotyped SNPs, and different distributions of age and sex. The code for simulation can easily be modified to introduce further imbalance/skewness with respect to sample size, number of SNPs, or even introduce differences in the number of causal variants per site.
<img src="./resources/Methods_simulationDetails.svg" alt="Parameters for generating synthetic data" width="300" height="300">
2. Explain the federated learning strategy
    - Spin up process on AWS. Install necessary requiremets on venv like nvflare, docker, etc.
    - Spin up processes on Brev (10 clients)
3. Explain the meta-analysis process
    - Use the global model to perform the final meta-analysis in each client site

## Results

## Future direction









## Topics

### 1. Synthetic data generation
- Genotypes
    - LD structure
    - Maybe sample from 1000 genomes?
    - Look at genotype simulators from the original gdoc
- Phenotype (0/1) - e.g., presence of Parkinson's disease
    - Take into account that if >1 phenotype, there is no covariance between phenotypes
- Assume that all have the same build (hg38)
- Generate in PLINK format (bed/bim/fam)
- Simulate per-site variability for genotypes and phenotypes

### 2. Federated learning infrastructure
- Server, client, admin specs (project.yml, NVFlare Dashboard on AWS)
- Set up the **FL server** on AWS
- ~10 Brev instances/**clients**
- Imbalance between sites of data distribution

### 3. Learning task
- Logistic regression model (sklearn-based)
- PyTorch model
- PLINK format


## Flow Chart

![flow-chart](./resources/Fed_learning_infrastructure.drawio.svg)
