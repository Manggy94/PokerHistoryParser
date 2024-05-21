#!/bin/bash

# Affiche un message pour indiquer le début des tests
echo "Running tests..."

# Dossier de référence pour la couverture
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


# Extraire le pourcentage total de couverture
total_coverage=$(grep 'TOTAL' coverage.txt | awk '{print $4}' | sed 's/%//')

# Vérifier si la couverture est supérieure ou égale à 90%
if (echo "$total_coverage >= 90" | bc -l); then
    echo "Test coverage is sufficient: ${total_coverage}%"
    exit 0
else
    echo "Test coverage is insufficient: ${total_coverage}%"
    exit 1
fi
