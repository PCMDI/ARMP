#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting installation..."

# Create a conda environment from the environment.yml file
if command -v conda >/dev/null 2>&1; then
    echo "Creating conda environment..."
    conda env create -f environment.yml  # Now it directly references the file in the same directory
else
    echo "Conda is not installed. Please install conda to proceed."
    exit 1
fi


# optional to install BlobStats

echo "Installation complete!"
