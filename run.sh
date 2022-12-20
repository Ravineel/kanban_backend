echo "Project will start running now ........."
echo "Please wait ................."
echo "............................."
if [ -d ".env" ];
then 
    echo "Virtual environment  exists and running it"
else
    echo "Create virtual environment using setup.sh"
    exit N
fi

source ./env/bin/activate
export ENV=Development
python app.py

echo "Project has started running ......."