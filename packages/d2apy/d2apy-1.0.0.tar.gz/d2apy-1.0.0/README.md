# d2-apy
python version of d2-api
# Generate build
python setup.py sdist bdist_wheel
# Push package
sudo twine upload dist/* --verbose -u user -p pass
