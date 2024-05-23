#!/bin/sh

# Check if the number of arguments is correct
if [ $# -ne 2 ]; then
  echo "Usage: $0 package_name project_name description"
  exit 1
fi

# Assign the arguments to variables
package_name=$1
project_name=$2

echo "Building Documentation Resources for $project_name"
#Install mkdocs if not installed
echo "Installing mkdocs and mkdocstrings"
if ! pip show mkdocs > /dev/null 2>&1 ; then
  echo "Installing mkdocs..."
  pip install mkdocs
else
  echo "mkdocs is already installed."
fi
if ! pip show mkdocstrings > /dev/null 2>&1 ; then
  echo "Installing mkdocstrings..."
  pip install mkdocstrings[python]
else
  echo "mkdocstrings is already installed."
fi
echo "Installing mkdocs: done"
echo ""

# Create mkdocs.yml
echo "Creating mkdocs.yml"

# Create the mkdocs.yml file from the template file
cp /mnt/c/users/mangg/template_files/mkdocs.yml mkdocs.yml

# Replace the placeholder with the project name
sed -i "s/project_name/$project_name/g" mkdocs.yml
echo "mkdocs.yml created successfully"
echo ""


# Make docs directory if it does not exist
if [ ! -d "docs" ]; then
  echo "Making docs directory"
  mkdir docs
else
  echo "docs directory already exists"
fi
echo "Making docs directory: done"
echo ""

# Create index.md in docs directory from the template file
echo "Creating index.md in docs directory"
cp /mnt/c/users/mangg/template_files/docs_index.md docs/index.md

# Replace the placeholder with the project name
sed -i "s/project_name/$project_name/g" docs/index.md
echo "index.md created successfully in docs directory"
echo ""

#Creating the docs/build_doc.sh script from the template
echo "Creating the scripts/build_doc.sh script"
cp /mnt/c/users/mangg/template_files/build_doc.sh scripts/build_doc.sh



