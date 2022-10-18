echo "Setup is now running ........."
echo "Please wait ................."
echo "............................."

# Install the required packages
sudo apt-get install -y python3.10
sudo apt-get install -y python3.10-pip
sudo apt-get install -y python3.10-venv

python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
deactivate

echo "Setup is now complete ......."

