# Installation
## Create a virtual environment
```
python -m venv venv
source venv/bin/activate
```

## Install dependencies
```
pip install -r requirements.txt
```

# Execution
## Plan a deployment
```
python main.py plan config/infrastructure.yaml
```

## Deploy a plan
```
python main.py apply config/infrastructure.yaml
```

## Destroy a plan
```
python main.py destroy config/infrastructure.yaml
```
