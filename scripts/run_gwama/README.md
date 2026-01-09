# GWAMA Meta-Analysis Docker Container

This container automates GWAS meta-analysis using GWAMA, converting REGENIE output to the required GWAMA format and performing meta-analysis across multiple sites.

## Quick Start

### Prerequisites

- Docker installed
- REGENIE output files (.regenie format) from each site

### Basic Usage

```bash
docker run --platform=linux/amd64 \
  -v /path/to/data:/data \
  ghcr.io/collaborativebioinformatics/gwama \
  <mode> <output_prefix> <site1_regenie> [site2_regenie] ...
```

docker run --platform=linux/amd64 -v /Users/espehage/Repositories/Fed_learning_infrastructure/resources/site1_gwas_results:/data -it ghcr.io/collaborativebioinformatics/gwama or gwama_meta /data/regenie_step2_Phen1.regenie

**Arguments:**
- `mode`: `or` for binary traits or `qt` for quantitative traits
- `output_prefix`: Prefix for output files
- `regenie_files`: Paths to REGENIE output files (use absolute paths)

### Example: Binary Trait (Case-Control)

```bash
docker run --platform=linux/amd64 \
  -v /Users/espehage/resources:/data \
  -v /Users/espehage/output:/output \
  ghcr.io/collaborativebioinformatics/gwama \
  or meta_analysis /data/site1.regenie /data/site2.regenie /data/site3.regenie
```

### Example: Quantitative Trait

```bash
docker run --platform=linux/amd64 \
  -v /Users/espehage/resources:/data \
  ghcr.io/collaborativebioinformatics/gwama \
  qt meta_results /data/site1.regenie /data/site2.regenie
```

## Important: Volume Mounting

The container **cannot access relative paths** from the host. You must:

1. Use **absolute paths** to data files
2. Mount directories with `-v /host/absolute/path:/container/path`
3. Reference files by their mounted paths inside the container

**❌ This will fail (relative paths don't work in containers):**
```bash
docker run ... gwama or meta ../../resources/site1.regenie
```

**✅ This works (absolute path or mounted volume):**
```bash
docker run -v /Users/espehage/resources:/data ... gwama or meta /data/site1.regenie
```

## Output Files

Results are saved in the container's `/work/gwama_analysis/` directory:

- `<output_prefix>.out` - Main GWAMA meta-analysis results
- `<output_prefix>.err.out` - Error log from GWAMA
- `<output_prefix>.in` - GWAMA input file list
- `<output_prefix>_site*.txt` - Converted GWAMA format files per site

To access results from your host, mount an output volume:

```bash
docker run --platform=linux/amd64 \
  -v /data/gwas:/input \
  -v /data/output:/output \
  ghcr.io/collaborativebioinformatics/gwama \
  or meta /input/site1.regenie /input/site2.regenie
```

Then retrieve results from `/output/`.

## Help

View the help message:

```bash
docker run ghcr.io/collaborativebioinformatics/gwama --help
```

## Building Locally

```bash
cd scripts/run_gwama
docker build --platform=linux/amd64 -t gwama:local -f Dockerfile.gwama .
docker run gwama:local or meta /data/site1.regenie
```

## Pipeline Steps

The entrypoint automatically:

1. **Converts** each site's REGENIE output to GWAMA format using `regenie_to_gwama.py`
2. **Creates** GWAMA input file list
3. **Runs** GWAMA meta-analysis with appropriate parameters for the trait type

## Manual Setup (if not using Docker)

### Download and build GWAMA

```bash
wget https://www.geenivaramu.ee/tools/GWAMA_v2.2.2.zip
unzip -d GWAMA GWAMA_v2.2.2.zip
cd GWAMA
make
chmod +x GWAMA
cd ..
```

### Convert Regenie output to GWAMA input format

```bash
export SITE=1
export DATA_PATH="../../resources/site${SITE}_gwas_results"
export FILEPREFIX="regenie_step2_Phen1.regenie"

python3 regenie_to_gwama.py \
    "${DATA_PATH}/${FILEPREFIX}" \
    "site${SITE}_for_gwama.txt" \
    "or"
```

### Create input file list for GWAMA

```bash
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

Please refer to https://genomics.ut.ee/en/tools for more details on interpreting GWAMA output files.


## Run GWAMA meta-analysis (test with mock data)

### run GWAS for each site (mock up data)

See instructions in `scripts/run_gwama/run_mock_gwas_w_plink/README.md`

```{bash}
cd scripts/run_gwama/run_mock_gwas_w_plink
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

Please refer to https://genomics.ut.ee/en/tools for more details on interpreting GWAMA output files.

## References

Mägi R, Morris AP. GWAMA: software for genome-wide association meta-analysis. BMC Bioinformatics. 2010 May 28;11:288. doi: 10.1186/1471-2105-11-288. PMID: 20509871; PMCID: PMC2893603.