echo "Setup is now running ........."
echo "Please wait ................."
echo "............................."

# Install the required packages
sudo apt-get install -y python3.8
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate

echo "Setup is now complete ......."

