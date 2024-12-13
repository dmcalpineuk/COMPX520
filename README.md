# COMPX520
git clone https://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@github.com/dmcalpineuk/COMPX520.git

cd COMPX520

sudo apt-get install libmysqlclient-dev

sudo pip install -r requirements.txt

python3 -m spacy download en_core_web_lg

python3 -m nltk.downloader stopwords

python3 ./main.py
