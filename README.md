# Update system
sudo yum update -y

# Install Python 3 and pip
sudo yum install python3 -y

# Ensure pip is installed
sudo yum install python3-pip -y

# Verify installation
python3 --version
pip3 --version

# Install Flask
pip3 install Flask

# Install MySQL connector
pip3 install mysql-connector-python
