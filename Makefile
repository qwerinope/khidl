build:
	python -m build --wheel --no-isolation

clean:
	rm -rv dist khinsider_dl.egg-info build

devbuild:
	make build
	pip install dist/*.whl --force-reinstall
	make clean
