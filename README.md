# Cipher Project

## Content of project
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [More detailed information about modules](#more-detailed-information-about-modules)

## General info

<b>Cipher project</b> was created to allow the user to encode/decode text based on the
Caesar cipher with rot13/rot47 (more information: [https://pl.wikipedia.org/wiki/Szyfr_Cezara](https://pl.wikipedia.org/wiki/Szyfr_Cezara)).

## Technologies and tools
<ul>
<li>Python 3.10</li>
<li>Pytest</li>
<li>Pre-commit</li>
</ul>

## Setup

Clone the repo:
```shell
git clone https://github.com/MatRos-sf/cipher
```
Create environment:
```shell
python -m venv venv
```
Install all the modules listed in the project requirements file:
```shell
pip install -r requirements.txt
```
Run project and enjoy:
```shell
python src/main.py
```

## More detailed information about modules

The project consists of 2 files: ```src``` and ```tests```. <b>The tests</b> file has all module tests.
<b>The src</b> file, on the other hand, contains all the modules that were used for the program to function.
Let's see what the src file consists of:
#### src/buffer
The buffer consists of 2 files: <b>buffer.py</b> and <b>text.py</b>.
In these files there are two important classes: ```Text``` it's a container of datum and ```Buffer``` which stores all ```Text``` objects.
#### src/ceaser
In this directory, there is a <b>Caesar</b> class that allows for both encryption and decryption code.
#### src/cipher
This directory contains the <b>Cipher</b> class, which is responsible for coordinating all the modules.
#### src/files
This directory contains all the saved files.
#### src/manager
This directory contains the <b>FileHandler</b> class, which is responsible for saving and reading files.
#### src/menu
This directory contains two important classes: <b>Executor</b> and <b>Menu</b>. The <b>Executor</b> is responsible for
running specific tasks, while the <b>Menu</b> allows for displaying available options that are executed through the <b>Executor</b> class.
#### src/main.py
It's the main script. If you run it, you will execute the program.
