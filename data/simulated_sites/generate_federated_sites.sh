#!/bin/bash
# Generate 10 federated learning sites with genomic data for Parkinson's disease

samples=(100000 95000 110000 88000 105000 92000 98000 103000 97000 101000)
nsnps=(500000 480000 520000 450000 510000 490000 505000 495000 515000 485000)

# LDAK binary path - update this to your local path
LDAK="./ldak6.1.mac"

echo "========================================"
echo "Federated Genomic Data Simulation"
echo "========================================"
echo ""

for site in {1..10}; do
  idx=$((site-1))
  mkdir -p site${site}

  echo "========================================"
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

  echo "Site ${site} complete!"
  echo ""
done

echo "========================================"
echo "All 10 sites generated successfully!"
echo "========================================"
echo ""
echo "Summary:"
for site in {1..10}; do
  echo "Site ${site}:"
  echo "  - Genotypes: site${site}/site${site}_geno.bed/bim/fam"
  echo "  - Phenotypes: site${site}/site${site}_pheno.pheno"
  echo "  - Covariates: site${site}/site${site}_geno.covar"
done