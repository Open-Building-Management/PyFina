# pour construire le package pip

Modifier le numéro de version dans setup.py

```
python3 setup.py sdist
python3 -m pip install wheel
python3 setup.py bdist_wheel
```
ces commandes créent un répertoire dist contenant un fichier tar.gz (sources) et un fichier wheel qui sera utilisé par pip

# pour envoyer le fichier sur pypi.org

on a besoin du package twine :
```
python3 -m pip install --user --upgrade twine
```

le plus pratique est de créer un fichier `.pypirc` dans son home, avec le contenu suivant : 
```
[pypi]
username = __token__
password = <the token value, including the `pypi-` prefix>
```
pour l'envoi :
```
python3 -m twine upload dist/*
```
le retour devrait être du genre suivant :
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading PyFina-0.0.1-py3-none-any.whl
100%|██████████████████████████████████████| 8.27k/8.27k [00:02<00:00, 3.30kB/s]
Uploading PyFina-0.0.1.tar.gz
100%|██████████████████████████████████████| 7.06k/7.06k [00:00<00:00, 7.88kB/s]

View at:
https://pypi.org/project/PyFina/0.0.1/
```
