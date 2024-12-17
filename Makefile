init: 
    pipenv install --dev

format: 
    pipenv run black mamaput_api tests

test: 
    pytest tests

coverage: 
    pytest --cov mamaput_api --cov-report term-missing tests