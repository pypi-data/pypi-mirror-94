<h1 align="center">
    PANGEAMT NLP
</h1>

<p align="left">
    <a href="http://52.16.81.128:5019/blue/organizations/jenkins/pangeamt-nlp/activity">
        <img alt="Jenkins tests" src="https://img.shields.io/jenkins/tests?compact_message&failed_label=failed%F0%9F%A4%A6%E2%80%8D%E2%99%80%EF%B8%8F&jobUrl=http%3A%2F%2F52.16.81.128%3A5019%2Fjob%2Fpangeamt-nlp%2Fjob%2Fmaster%2F&passed_label=passed%20%20%F0%9F%91%8D">
    </a>
    <a href="https://pypi.org/project/pangeamt-nlp/">
        <img alt="GitHub release" src="https://img.shields.io/pypi/v/pangeamt-nlp">
    </a>
</p>

### How to update and upload to PyPi

1. In the terminal go to the pangeamt_nlp directory.

2. Switch to the branch that made the PR:
```
git checkout <source_branch>
git pull
```
3. Activate the virtual env:
```
source venv/bin/activate
```
4. Remove the previous packages created:
```
rm -r dist
```
5. Create the package source distribution:
```
python setup.py sdist
```
7. Install the new distribution:
```
pip install dist/*
```
6. Test the changes:
```
cd tests
```
```
python -m unittest
```
7. If it passes the tests accept the PR in github webpage.

8. Change to the master branch:
```
git checkout master
git pull
```
9. Increment version number:
```
vim pangeamt_nlp/__init__.py
git add pangeamt_nlp/__init__.py
git commit -m "Update version number"
git push
```
10. Delete older distributions:
```
rm -r dist/*
```
11. Create source and binary distributions:
```
python setup.py sdist bdist_wheel
```
12. Upload distributions to PyPi:
```
twine upload dist/*
```
