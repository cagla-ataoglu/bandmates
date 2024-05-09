#!/bin/bash

# Make it executable:
# chmod +x run_test.sh

# Command to run tests with coverage report:
# ./run_test.sh

# Script exits on error
set -e

# Set PYTHONPATH to include the root of the project
export PYTHONPATH=$(pwd)

# Find all test files with "test" in their names
TEST_FILES=$(find . -name "test*.py")

# Define the source path to include the entire project directory
PROJECT_DIR="."

# Run unit tests with coverage
coverage run --source=${PROJECT_DIR} -m unittest -v ${TEST_FILES}

# Generate coverage reports
echo "Generating coverage report..."
coverage report -m

echo "Generating HTML report..."
coverage html

echo "All tests executed. Coverage report available in 'htmlcov/index.html'."
