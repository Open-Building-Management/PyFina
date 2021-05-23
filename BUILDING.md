# pour construire le package pip

```
python3 setup.py sdist
python3 -m pip install wheel
python3 setup.py bdist_wheel
```
ces commandes créent un répertoire dist contenant un fichier tar.gz (sources) et un fichier wheel qui sera utilisé par pip

# pour envoyer le fichier sur pypi.org

le plus pratique est de créer un fichier `.pypirc` dans son home, avec le contenu suivant : 
```
[pypi]
username = __token__
password = <the token value, including the `pypi-` prefix>
```
