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
rs_number	reference_allele	other_allele	eaf	OR	OR_se	OR_95L	OR_95U	z	p-value	_-log10_p-value	q_statistic	q_p-value	i2	n_studies	n_samples	effects
SNP1	A	C	-9	0.884922	0.097971	0.692897	1.130162	-0.979582	0.327281	0.485080	0.248941	0.617821	0.000000	2	-9	--
SNP2	A	C	-9	0.976209	0.136775	0.708129	1.345777	-0.146998	0.883115	0.053983	0.321468	0.570727	0.000000	2	-9	+-
SNP3	A	C	-9	0.969469	0.122319	0.729723	1.287981	-0.213930	0.830592	0.080612	0.674754	0.411399	0.000000	2	-9	-+
...
``` 
