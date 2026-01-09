#!/bin/bash

set -euo pipefail

# GWAMA meta-analysis entrypoint
# Converts REGENIE results to GWAMA format and runs meta-analysis
#
# Usage:
#   entrypoint.gwama.sh <mode> <output_prefix> <site1_regenie_file> [site2_regenie_file] ...
#
# Arguments:
#   mode: 'or' for odds ratio (case-control) or 'qt' for quantitative trait
#   output_prefix: prefix for GWAMA output files
#   regenie_files: paths to .regenie output files (one per site)
#
# Example:
#   entrypoint.gwama.sh or gwama_results /data/site1.regenie /data/site2.regenie

# Show help
if [ $# -eq 0 ] || [[ "$1" == "--help" || "$1" == "-h" ]]; then
    cat << 'EOF'
GWAMA Meta-Analysis Pipeline

Usage:
  entrypoint.gwama.sh <mode> <output_prefix> <site1_regenie_file> [site2_regenie_file] ...

Arguments:
  mode: 'or' for odds ratio (case-control) or 'qt' for quantitative trait
  output_prefix: prefix for GWAMA output files
  regenie_files: paths to .regenie output files (one per site, use absolute paths or mount volumes)

Example:
  docker run -v /path/to/data:/data ghcr.io/collaborativebioinformatics/gwama \
    or gwama_results /data/site1.regenie /data/site2.regenie

Note:
  Use absolute paths or mount input data with -v flag. Relative paths from host do not work in containers.
EOF
    exit 0
fi

if [ $# -lt 3 ]; then
    echo "Error: Insufficient arguments"
    echo "Usage: $0 <mode> <output_prefix> <site1_regenie_file> [site2_regenie_file] ..."
    echo "Run with --help for more information"
    exit 1
fi

mode="$1"
output_prefix="$2"
shift 2
regenie_files=("$@")

# Validate mode
if [[ ! "$mode" =~ ^(or|qt)$ ]]; then
    echo "Error: mode must be 'or' or 'qt', got '$mode'"
    exit 1
fi

echo "======================================"
echo "GWAMA Meta-Analysis Pipeline"
echo "======================================"
echo "Mode: $mode"
echo "Output prefix: $output_prefix"
echo "Number of sites: ${#regenie_files[@]}"
echo ""

# Create working directory
WORKDIR="/work/gwama_analysis"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# Convert each site's REGENIE output to GWAMA format
echo "Step 1: Converting REGENIE outputs to GWAMA format..."
gwama_input_files=()

for i in "${!regenie_files[@]}"; do
    site_num=$((i + 1))
    input_file="${regenie_files[$i]}"
    output_file="${output_prefix}_site${site_num}.txt"

    if [ ! -f "$input_file" ]; then
        echo "Error: Input file not found: $input_file"
        echo ""
        echo "Troubleshooting:"
        echo "  - Ensure file exists at the specified path"
        echo "  - Use absolute paths inside the container"
        echo "  - Mount data directory with: docker run -v /host/path:/data ..."
        echo "  - Then reference files as: /data/filename"
        exit 1
    fi

    echo "  Site $site_num: Converting $input_file..."
    python3 /tools/regenie_to_gwama.py "$input_file" "$output_file" "$mode"
    gwama_input_files+=("$output_file")
done

echo ""
echo "Step 2: Creating GWAMA input file list..."
gwama_input_list="${output_prefix}.in"
for file in "${gwama_input_files[@]}"; do
    echo "$file" >> "$gwama_input_list"
done
echo "Created: $gwama_input_list"
echo ""

echo "Step 3: Running GWAMA meta-analysis..."
if [ "$mode" == "or" ]; then
    GWAMA \
        -i "$gwama_input_list" \
        --output "$output_prefix" \
        --name_marker MARKERNAME \
        --name_ea EA \
        --name_nea NEA \
        --name_or OR \
        --name_or_95l OR_95L \
        --name_or_95u OR_95U
else
    # Quantitative trait mode (no OR fields)
    GWAMA \
        -i "$gwama_input_list" \
        --output "$output_prefix" \
        --name_marker MARKERNAME \
        --name_ea EA \
        --name_nea NEA
fi

echo ""
echo "======================================"
echo "GWAMA meta-analysis completed!"
echo "======================================"
echo "Results saved to: $WORKDIR"
echo "  - Main output: ${output_prefix}.out"
echo "  - Error log: ${output_prefix}.err.out"
echo ""
