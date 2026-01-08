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
1. Synthetic data generation process

We generated realistic synthetic dataset for 10 different sites using the LDAK software [https://dougspeed.com/downloads/]. Specifically, the simulated phenotype was a case-control phenotype representing the case status of having Parkinson's Disease with a realistic population prevalence rate of 1%, single nucleotide polymorphism (SNP) heritability of 0.25 (on a liability scale), 20 causal SNPs per site, and using the "LDAK-Thin" effect size model with a power of -0.25. For each site, the covariates included age and sex that overall explained ~10% of the phenotypic variance. For the genotype simulation., we allowed the number of SNPs to vary between ~450,000 to ~520,000 variants per site while the sample size per site varied between 88,000 and 110,000. This resulted in synthetic data across 10 sites with varied number of subjects, slightly different number of genotyped SNPs, and different distributions of age and sex. The code for simulation can easily be modified to introduce further imbalance/skewness with respect to sample size, number of SNPs, or even introduce differences in the number of causal variants per site.

<img src="./resources/Methods_simulationDetails.svg" alt="Parameters for generating synthetic data" width="600" height="600">

2. Federated learning strategy

Federated learning was implemented using a centralized server–client architecture orchestrated with NVFlare. The federated server was deployed on an AWS compute instance and served as the coordinator for model aggregation, round management, and secure communication. A dedicated Python virtual environment (venv) was created on the AWS instance to ensure dependency isolation and reproducibility. The server process was initialized using NVFlare’s provisioning and startup utilities and remained persistently active throughout training to manage federated rounds and aggregate client updates. Federated clients were deployed across ten independent compute instances provisioned using Brev. Each client ran inside a Docker container to ensure environmental consistency across heterogeneous hardware. Client containers were built from a common Docker image that defined a venv with identical package versions to those used by the server where applicable, including nvflare 2.7.1. During runtime, each client container connected to the central AWS-hosted server and participated in synchronous federated learning rounds by locally training the model on its private data and transmitting only model parameters back to the server, without any raw data leaving the client environments.

<img src="./resources/fl_architecture.png" alt="FL architecture" width="900" height="500">

3. Meta-analysis (aggregation)


Within the GWAS world, there are two well-established approaches for performing meta-analysis ("aggregation" across sites): fixed-effects meta-analysis and random-effects meta analysis. Once we have performed GWASes for each site, the summary statistics include the beta coefficient and the standard error, for each genetic variant. Then, the fixed-effects approach to getting an aggregate effect size is to do an inverse variance weighted-summing of the beta coefficients to get an overall effect size. However, this approach does not account for between-study (or between-site) variances. The random-effects meta-analysis approach explicitly accounts for between-site variance by explicitly including a variance component, estimated based on heterogeniety test. In our approach, we allow the users to perform both types of meta-analyses. The random effects meta-analysis is implemented via a call to the GWAMA software (Magi et al., 2010). In practical terms, the output from the site-specific GWASes are first re-organised to meet the GWAMA required format; then, within the aggregator function, we perform a system call to the GWAMA tool, and finally, reformat the output from GWAMA to match the requirements for NVFLARE ecosystem.

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
