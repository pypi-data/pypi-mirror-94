sts models

model objects have their attributes defined in camelCase to align with what is normal in javascript (and JSON).


use python3 setup.py sdist bdist_wheel to make new version
then remove old whl and tar files
then use ```python3 -m twine upload --repository testpypi dist/*``` to reupload

then, in the project the library is to be used in, do
pip uninstall <name>
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple <name>
to get the latest

once the dependency is solidified, you don't have to use test.pypi, so instead, the above becomes:

use python3 setup.py sdist bdist_wheel to make new version
then remove old whl and tar files
then use ```python3 -m twine upload dist/*``` to reupload

then, in the project the library is to be used in, do
pip uninstall <name>
pip install <name>
to get the latest

Don't forget to save the dependency snapshot in this and the other package!
pip freeze > requirements.txt
