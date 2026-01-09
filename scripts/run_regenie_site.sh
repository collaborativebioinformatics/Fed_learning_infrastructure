#!/bin/bash
# Run REGENIE Step 1 and Step 2 on a specific federated learning site using Docker

# Check if site number provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/run_regenie_site.sh <site_number>"
    echo "Example: ./scripts/run_regenie_site.sh 1"
    exit 1
fi

SITE_NUM=$1
SITE_DIR="./data/simulated_sites/site${SITE_NUM}"
REGENIE_IMAGE="ghcr.io/rgcgithub/regenie/regenie:v4.1.gz"

# Get absolute path for Docker volume mount
ABSOLUTE_SITE_DIR="$(cd "$(dirname "${SITE_DIR}")" && pwd)/$(basename "${SITE_DIR}")"

# Check if site directory exists
if [ ! -d "${SITE_DIR}" ]; then
    echo "Error: Site ${SITE_NUM} directory not found: ${SITE_DIR}"
    echo "Run './scripts/download_site_from_s3.sh ${SITE_NUM}' first to download the data"
    exit 1
fi

echo "========================================"
echo "Running REGENIE on Site ${SITE_NUM}"
echo "========================================"

# Step 1: Build prediction model with LOCO
echo ""
echo "Step 1: Building LOCO prediction model..."
echo "This may take 15-30 minutes..."
echo ""

docker run --rm \
  -v ${ABSOLUTE_SITE_DIR}:/data \
  ${REGENIE_IMAGE} \
  regenie \
  --step 1 \
  --bed /data/site${SITE_NUM}_geno \
  --phenoFile /data/site${SITE_NUM}_pheno.pheno \
  --covarFile /data/site${SITE_NUM}_geno.covar \
  --bsize 1000 \
  --bt \
  --lowmem \
  --out /data/regenie_step1

# Check if Step 1 succeeded
if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Step 1 failed for Site ${SITE_NUM}"
    exit 1
fi

echo ""
echo "✓ Step 1 complete"
echo ""

# Verify Step 1 outputs exist
if [ ! -f "${SITE_DIR}/regenie_step1_pred.list" ]; then
    echo "✗ Step 1 prediction file not found"
    exit 1
fi

# Step 2: Association testing
echo "Step 2: Running genome-wide association testing..."
echo "This may take 10-20 minutes..."
echo ""

docker run --rm \
  -v ${ABSOLUTE_SITE_DIR}:/data \
  ${REGENIE_IMAGE} \
  regenie \
  --step 2 \
  --bed /data/site${SITE_NUM}_geno \
  --phenoFile /data/site${SITE_NUM}_pheno.pheno \
  --covarFile /data/site${SITE_NUM}_geno.covar \
  --bt \
  --firth --approx \
  --pred /data/regenie_step1_pred.list \
  --bsize 400 \
  --out /data/regenie_step2

# Check if Step 2 succeeded
if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Step 2 failed for Site ${SITE_NUM}"
    exit 1
fi

echo ""
echo "✓ Step 2 complete"
echo ""

echo "========================================"
echo "REGENIE Analysis Complete for Site ${SITE_NUM}"
echo "========================================"
echo ""
echo "Output files:"
ls -lh ${SITE_DIR}/regenie_step1* ${SITE_DIR}/regenie_step2* 2>/dev/null
echo ""
echo "Association results: ${SITE_DIR}/regenie_step2_*.regenie"
echo ""
echo "Top associations:"
echo "----------------"
head -20 ${SITE_DIR}/regenie_step2_*.regenie