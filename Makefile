install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:	
	black *.py 

lint:
	pylint check *.py mylib/*.py

test:
	python -m pytest -vv -cov=mylib test_*.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	#deploy goes here
		
all: install lint test format deploy