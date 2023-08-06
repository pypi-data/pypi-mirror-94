clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-test: ## remove test artifacts
	rm -fr .tox/
	rm -fr .pytest_cache/
	rm -fr htmlcov/

clean: clean-build clean-test

dist: clean-build ## builds source and wheel package
	python setup.py sdist bdist_wheel

release: dist ## package and upload a release
	python -m twine upload dist/*