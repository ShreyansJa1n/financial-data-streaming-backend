# script that accepts a package name and installs it using pip
#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: $0 <package_name>"
    exit 1
fi

PACKAGE_NAME=$1
echo "Installing package: $PACKAGE_NAME"
# Check if the virtual environment exists
if [ ! -d "./.venv" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment."
        exit 1
    fi
fi
# Activate the virtual environment
source ./.venv/bin/activate

# Install the package using pip
pip install "$PACKAGE_NAME"
if [ $? -eq 0 ]; then
    echo "Package $PACKAGE_NAME installed successfully."
else
    echo "Failed to install package $PACKAGE_NAME."
    exit 1
fi

pip freeze > ./requirements/requirements.txt
echo "Updated requirements.txt with installed packages."
# Deactivate the virtual environment
deactivate
echo "Virtual environment deactivated."
# End of script
