# README

## download and build gwama

```bash
wget https://www.geenivaramu.ee/tools/GWAMA_v2.2.2.zip
unzip -d GWAMA GWAMA_v2.2.2.zip
cd GWAMA
make
chmod +x GWAMA
cd ..
```

## Run GWAMA meta-analysis

### run GWAS for each site (mock up)
```bash
cd data/run_mock_gwas_w_plink
bash run_gwas.sh    
```

### create input file list for GWAMA

```bash
$ cat gwama.in
../run_mock_gwas_w_plink/gwas_site1_for_gwama.txt
../run_mock_gwas_w_plink/gwas_site2_for_gwama.txt
```

### run GWAMA

```bash
# Meta-analysis using GWAMA
./GWAMA/GWAMA \
    -i gwama.in \
    --output gwama.out \
    -qt \
    --name_marker MARKERNAME \
    --name_ea EA \
    --name_nea NEA \
    --name_or OR \
    --name_or_95l OR_95L \
    --name_or_95u OR_95U
```

Output:
```bash
$ head gwama.out.out
rs_number	reference_allele	other_allele	eaf	beta	se	beta_95L	beta_95U	z	p-value	_-log10_p-value	q_statistic	q_p-value	i2	n_studies	n_samples	effects
SNP1	A	C	-9	-0.122257	0.124807	-0.366878	0.122365	-0.979567	0.327288	0.485070	0.248932	0.617828	0.000000	2	-9	--
SNP2	A	C	-9	-0.024078	0.163804	-0.345134	0.296977	-0.146995	0.883117	0.053982	0.321458	0.570733	0.000000	2	-9	+-
SNP3	A	C	-9	-0.031008	0.144943	-0.315096	0.253081	-0.213929	0.830592	0.080612	0.674725	0.411409	0.000000	2	-9	-+
...
``` 
