run:
	python main.py

isort:
	isort .
	
run_with_isort: isort run