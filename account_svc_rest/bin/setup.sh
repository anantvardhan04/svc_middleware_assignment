#!/bin/bash
set -e

# Create a virtual environment
echo "Creating virtual environment..."
python -m venv .venv
. .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set up the database
echo "Setting up the database..."
python -m app.seed

# Install Rabbit mq
echo "Installing RabbitMQ..."
sh bin/install_rabbitmq.sh

echo "Setting up rabbitmq queues and exchanges..."
python -m app.rabbitmq_setup

echo "Setup complete!"
echo "Starting the account service..."

# Run the application
export FLASK_APP=app
flask run