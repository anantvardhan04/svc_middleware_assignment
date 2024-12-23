#!/bin/bash
set -e

# Create a virtual environment
echo "Creating virtual environment..."
python -m venv .venv
. .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo "Starting the account grpc server..."

# Run the application
python main.py