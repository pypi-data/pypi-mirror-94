# Butiran Package
Python package for simulation of grain-based system


## test a module
```
py>cd tests
py\tests>py vect3_tests.py
Test for class Vect3
a = (0, 3, 4)
|a| = 5.0
-b = (0, -3, -4)
^b = (0.0, -0.6, -0.8)
a + b = (0, 0, 0)
a - b = (0, 6, 8)
e = (2, 0, 0)
e x a = (0, -8, 6)

py\tests>
```


## build distribution
```
py>py setup.py sdist bdist_wheel
running sdist
running egg_info
writing butiran.egg-info\PKG-INFO
writing dependency_links to butiran.egg-info\dependency_links.txt
writing requirements to butiran.egg-info\requires.txt
writing top-level names to butiran.egg-info\top_level.txt
reading manifest file 'butiran.egg-info\SOURCES.txt'
writing manifest file 'butiran.egg-info\SOURCES.txt'
running check
creating butiran-0.0.2
creating butiran-0.0.2\butiran.egg-info
copying files to butiran-0.0.2...
copying README.md -> butiran-0.0.2
copying pyproject.toml -> butiran-0.0.2
copying setup.py -> butiran-0.0.2
copying butiran.egg-info\PKG-INFO -> butiran-0.0.2\butiran.egg-info
copying butiran.egg-info\SOURCES.txt -> butiran-0.0.2\butiran.egg-info
copying butiran.egg-info\dependency_links.txt -> butiran-0.0.2\butiran.egg-info
copying butiran.egg-info\requires.txt -> butiran-0.0.2\butiran.egg-info
copying butiran.egg-info\top_level.txt -> butiran-0.0.2\butiran.egg-info
Writing butiran-0.0.2\setup.cfg
Creating tar archive
removing 'butiran-0.0.2' (and everything under it)
running bdist_wheel
running build
installing to build\bdist.win-amd64\wheel
running install
running install_egg_info
Copying butiran.egg-info to build\bdist.win-amd64\wheel\.\butiran-0.0.2-py3.9.egg-info
running install_scripts
adding license file "LICENSE" (matched pattern "LICEN[CS]E*")
creating build\bdist.win-amd64\wheel\butiran-0.0.2.dist-info\WHEEL
creating 'dist\butiran-0.0.2-py3-none-any.whl' and adding 'build\bdist.win-amd64\wheel' to it
adding 'butiran-0.0.2.dist-info/LICENSE'
adding 'butiran-0.0.2.dist-info/METADATA'
adding 'butiran-0.0.2.dist-info/WHEEL'
adding 'butiran-0.0.2.dist-info/top_level.txt'
adding 'butiran-0.0.2.dist-info/RECORD'
removing build\bdist.win-amd64\wheel

py>
```


## upload package
```
py>py -m twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: dudung
Enter your password:
Uploading butiran-0.0.2-py3-none-any.whl
100%|██████████████████████████████████████████████| 5.68k/5.68k [00:04<00:00, 1.30kB/s]
Uploading butiran-0.0.2.tar.gz
100%|██████████████████████████████████████████████| 5.71k/5.71k [00:01<00:00, 3.19kB/s]

View at:
https://pypi.org/project/butiran/0.0.2/

py>
```


## version
```
py>py --version
Python 3.9.1

py>py -m twine --version
twine version 3.3.0 (pkginfo: 1.7.0, requests: 2.25.1, setuptools: 49.2.1, requests-
toolbelt: 0.9.1, tqdm: 4.56.0)

py>
```
HTTPError: 400 Bad Request from https://upload.pypi.org/legacy/
File already exists. See https://pypi.org/help/#file-name-reuse for more information.

ERROR: Could not find a version that satisfies the requirement python>=3.6 (from butiran)
ERROR: No matching distribution found for python>=3.6


HTTPError: 400 Bad Request from https://test.pypi.org/legacy/
File already exists. See https://test.pypi.org/help/#file-name-reuse for more information

ERROR: Could not find a version that satisfies the requirement python>=3.6 (from butiran)
ERROR: No matching distribution found for python>=3.6