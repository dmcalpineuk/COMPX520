# COMPX520
git clone https://github.com/dmcalpineuk/COMPX520.git

cd COMPX520

sudo apt-get install libmysqlclient-dev

sudo pip install -r requirements.txt

python3 -m spacy download en_core_web_lg

python3 -m nltk.downloader stopwords

python3 ./main.py
