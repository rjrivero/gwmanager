#!/usr/bin/env bash
# -------------------------------------------
# inicializa el entorno para ejecutar ansible
# Este script debe invocarse en el directorio
# del virtualenv, con
#
# . ./init.sh
#
# o
#
# source ./init.sh
# -------------------------------------------

export VIRTUALENV_PATH=~/virtualenvs/ansible

# Para actualizar ansible:
function update {
    pip install -U paramiko PyYAML Jinja2 httplib2
    pushd .
    cd ansible
    git pull --rebase
    git submodule update --init --recursive
    popd
}

# Entrar al virtualenv
cd "$VIRTUALENV_PATH"
source bin/activate

# Activar el entorno de ansible
source ansible/hacking/env-setup

# Variables de entorno que necesito
export PUB_KEYS_DIR="$VIRTUALENV_PATH/inventory/pub_keys"
export ANSIBLE_INVENTORY="$VIRTUALENV_PATH/inventory/hosts"
export ANSIBLE_CONFIG="$VIRTUALENV_PATH/inventory/ansible.cfg"
export ANSIBLE_LIBRARY="$VIRTUALENV_PATH/inventory/library"

# Si se nos pasa "-U" en la linea de comandos, actualizar
if [ "x$1" == "x-U" ]; then
    update
fi
