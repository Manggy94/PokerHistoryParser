#!/bin/bash

# Display a message to indicate the beginning of the tests
echo "Running tests..."

# Reference directory for coverage
SOURCE_DIRS="pkrhistoryparser"

# Execute tests
coverage run --source=$SOURCE_DIRS -m unittest discover -s tests -p "test_*.py"

# Check if tests failed
if [ $? -ne 0 ]; then
    echo "Tests failed."
    exit 1
fi

# Generate coverage report
coverage report > coverage.txt


# Extract the total coverage percentage
total_coverage=$(grep 'TOTAL' coverage.txt | awk '{print $4}' | sed 's/%//')
coverage html

# Check if the coverage is greater than or equal to 75%
if [ $(echo "$total_coverage >= 50" | bc -l) -eq 1 ]  ; then
    echo "Test coverage is sufficient: ${total_coverage}%"
    exit 0
else
    echo "Test coverage is insufficient: ${total_coverage}%"
    # Afficher le rapport de couverture en html
    exit 1
fi
