if [ -d venv ]; then
   echo "venv is found, running the app"
   source venv/bin/activate
   python main.py
else
   echo "venv is not found, creating venv and downloading the libs..."
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   echo "done. running the app"
   python main.py
fi
