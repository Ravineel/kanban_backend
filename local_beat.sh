echo "Project will start running now ........."
echo "Please wait ................."
echo "............................."
if [ -d "env" ];
then 
    echo "Virtual environment  exists and running it"
else
    echo "Create virtual environment using setup.sh"
    exit N
fi

celery -A app.celery beat --max-interval 1 -l info

echo "workers have started running ......."