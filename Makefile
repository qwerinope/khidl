build:
	python -m build --wheel --no-isolation

clean:
	rm -rv dist khidl.egg-info build

devbuild:
	make build
	pip install dist/*.whl --force-reinstall
	make clean
