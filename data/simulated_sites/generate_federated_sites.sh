#!/bin/bash
# Generate a single federated learning site with genomic data for Parkinson's disease
# Usage: ./generate_federated_sites.sh <site_number>
# Example: ./generate_federated_sites.sh 1

samples=(100000 95000 110000 88000 105000 92000 98000 103000 97000 101000)
nsnps=(500000 480000 520000 450000 510000 490000 505000 495000 515000 485000)

# Check if site number is provided
if [ $# -eq 0 ]; then
  echo "Error: Site number required"
  echo "Usage: $0 <site_number>"
  echo "Example: $0 1"
  echo "Site number must be between 1 and 10"
  exit 1
fi

site=$1

# Validate site number
if ! [[ "$site" =~ ^[0-9]+$ ]] || [ "$site" -lt 1 ] || [ "$site" -gt 10 ]; then
  echo "Error: Site number must be between 1 and 10"
  exit 1
fi

# LDAK binary path - update this to your local path
case "$(uname -s)" in
    Darwin)
        export OS_TYPE="mac"
        ;;
    Linux*)
        export OS_TYPE="linux"
        ;;
    *)
        echo $"Unsupported OS. Please use macOS or Linux."
        exit 1
        ;;
esac

LDAK="./ldak6.1.${OS_TYPE}"

idx=$((site-1))
mkdir -p site${site}

echo "========================================"
echo "Federated Genomic Data Simulation"
echo "========================================"
echo ""
echo "Generating site ${site}: ${samples[$idx]} samples, ${nsnps[$idx]} SNPs"
echo "========================================"

# Generate genotypes (auto-creates .covar file)
echo "Step 1: Generating genotypes..."
$LDAK \
  --make-snps site${site}/site${site}_geno \
  --num-samples ${samples[$idx]} \
  --num-snps ${nsnps[$idx]}

# Generate Parkinson's disease phenotypes
echo "Step 2: Generating Parkinson's phenotypes..."
$LDAK \
  --make-phenos site${site}/site${site}_pheno \
  --bfile site${site}/site${site}_geno \
  --her 0.25 \
  --prevalence 0.01 \
  --num-causals 20 \
  --power -0.25 \
  --num-phenos 1 \
  --covar site${site}/site${site}_geno.covar \
  --covar-her 0.1

echo ""
echo "========================================"
echo "Site ${site} generated successfully!"
echo "========================================"
echo ""
echo "Generated files:"
echo "  - Genotypes: site${site}/site${site}_geno.bed/bim/fam"
echo "  - Phenotypes: site${site}/site${site}_pheno.pheno"
echo "  - Covariates: site${site}/site${site}_geno.covar"