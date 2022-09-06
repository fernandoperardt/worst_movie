# Worst Movie

## Requirents
* Python
* Pip
* Virtualenv

## Install dependencies
```
virtualenv venv
source venv/bin/activate
pip install --no-cache-dir --upgrade -r requirements.txt
```

## How run
APP: First migrate than run
```
make migrate-up
make dev
```

Test:
```
make test
```

## How use other csv file to load
Replace app/pre_load.csv for a valid csv