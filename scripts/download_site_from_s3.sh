#!/bin/bash
# Download federated learning site data from S3

# Check if site number provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/download_site_from_s3.sh <site_number>"
    echo "Example: ./scripts/download_site_from_s3.sh 1"
    exit 1
fi

SITE_NUM=$1
S3_BASE_URI="s3://flsynthdata/sitesdata"
LOCAL_DIR="./data/simulated_sites/site${SITE_NUM}"

echo "========================================"
echo "Downloading Site ${SITE_NUM} from S3"
echo "========================================"

# Create local directory
mkdir -p ${LOCAL_DIR}

# Download data from S3
echo "Downloading from ${S3_BASE_URI}/site${SITE_NUM}/ ..."
echo ""

aws s3 sync ${S3_BASE_URI}/site${SITE_NUM}/ ${LOCAL_DIR}/ \
    --exclude "*" \
    --include "*.bed" \
    --include "*.bim" \
    --include "*.fam" \
    --include "*.pheno" \
    --include "*.covar"

# Check if download was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Successfully downloaded Site ${SITE_NUM} data (~15 GB)"
    echo ""
    echo "Downloaded files:"
    ls -lh ${LOCAL_DIR}/
    echo ""
else
    echo ""
    echo "✗ Error downloading Site ${SITE_NUM} data"
    echo "Make sure AWS CLI is configured: aws configure"
    exit 1
fi

echo "========================================"
echo "Site ${SITE_NUM} ready for analysis"
echo "========================================"