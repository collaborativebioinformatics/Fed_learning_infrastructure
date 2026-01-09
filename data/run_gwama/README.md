# Run GWAMA meta-analysis

## Download and build GWAMA

The `GWAMA` binary need to exist on the server site where the meta-analysis is run.

```{bash}
wget https://www.geenivaramu.ee/tools/GWAMA_v2.2.2.zip
unzip -d GWAMA GWAMA_v2.2.2.zip
cd GWAMA
make
chmod +x GWAMA
cd ..
```

## Run GWAMA meta-analysis (Regenie data format)

### Convert Regenie output to GWAMA input format

```{bash}
export SITE=1
export DATA_PATH="../../resources/site${SITE}_gwas_results"
export FILEPREFIX="regenie_step2_Phen1.regenie"

python3 regenie_to_gwama.py  \
    "${DATA_PATH}/${FILEPREFIX}" \
    "site${SITE}_for_gwama.txt" \
    "or"
```

### create input file list for GWAMA

Should contain data from all 10 sites, here shown for site 1 only for brevity.

```{bash}
echo site1_for_gwama.txt > gwama.in
```

### run GWAMA

```{bash}
# Meta-analysis using GWAMA
./GWAMA/GWAMA \
    -i gwama.in \
    --output gwama \
    --name_marker MARKERNAME \
    --name_ea EA \
    --name_nea NEA \
    --name_or OR \
    --name_or_95l OR_95L \
    --name_or_95u OR_95U
```

### Output

```{bash}
rs_number	reference_allele	other_allele	eaf	OR	OR_se	OR_95L	OR_95U	z	p-value	_-log10_p-value	q_statistic	q_p-value	i2	n_studies	n_samples	effects
SNP1	A	C	-9	0.981198	0.044274	0.894420	1.076395	-0.401764	0.687875	0.162490	-0.000000	1.000000	0.000000	1	-9	-
SNP2	A	C	-9	1.104753	0.049437	1.007857	1.210964	2.127103	0.033432	1.475837	-0.000000	1.000000	0.000000	1	-9	+
SNP3	A	C	-9	1.016838	0.058183	0.902800	1.145280	0.275127	0.783218	0.106117	0.000000	1.000000	nan	1	-9	+
...
```

## Run GWAMA meta-analysis (test with mock data)

### run GWAS for each site (mock up data)

See instrunctions in `data/run_mock_gwas_w_plink/README.md`

```{bash}
cd data/run_gwama/run_mock_gwas_w_plink
bash run_gwas.sh
cd ..   
```

### create input file list for GWAMA

```{bash}
cat gwama.in
run_mock_gwas_w_plink/gwas_site1_for_gwama.txt
run_mock_gwas_w_plink/gwas_site2_for_gwama.txt
```

### run GWAMA

```{bash}
# Meta-analysis using GWAMA
./GWAMA/GWAMA \
    -i gwama.in \
    --output gwama \
    --name_marker MARKERNAME \
    --name_ea EA \
    --name_nea NEA \
    --name_or OR \
    --name_or_95l OR_95L \
    --name_or_95u OR_95U
```

Output:
```{bash}
$ head gwama.out
rs_number	reference_allele	other_allele	eaf	OR	OR_se	OR_95L	OR_95U	z	p-value	_-log10_p-value	q_statistic	q_p-value	i2	n_studies	n_samples	effects
SNP1	A	C	-9	0.884922	0.097971	0.692897	1.130162	-0.979582	0.327281	0.485080	0.248941	0.617821	0.000000	2	-9	--
SNP2	A	C	-9	0.976209	0.136775	0.708129	1.345777	-0.146998	0.883115	0.053983	0.321468	0.570727	0.000000	2	-9	+-
SNP3	A	C	-9	0.969469	0.122319	0.729723	1.287981	-0.213930	0.830592	0.080612	0.674754	0.411399	0.000000	2	-9	-+
...
``` 