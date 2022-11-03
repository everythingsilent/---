conda create --name fatigue_detection python=3.6
python -m pip install --upgrade pip
pip install pyqt5==5.15.6
pip install dlib==19.6.1
pip install opencv-python==4.5.4.60


conda activate fatigue_detecion
python mainWindow.py