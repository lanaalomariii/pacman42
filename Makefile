.PHONY: install run debug clean lint package pclean

install:
	python3 -m venv venv
	venv/bin/pip install mypy flake8 pygame pyinstaller
	venv/bin/pip install  mazegenerator-2.1.0-py3-none-any.whl

run:
	python3 pac-man.py config.json

debug:
	python3 -m pdb pac-man.py config.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache
	rm -rf venv
lint:
	flake8 . --exclude=venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

package:
	pyinstaller --onefile pac-man.py
	cp -r graphics dist/
	cp config.json dist/
pclean:
	rm -rf build dist *.spec
