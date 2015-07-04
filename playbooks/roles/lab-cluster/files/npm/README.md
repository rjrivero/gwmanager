Instrucciones
=============

Dar de alta usuarios
--------------------

    npm install -g htpasswd
    htpasswd -c npm.htpasswd username

Usar el registro
----------------

    npm set registry http://{{ REGISTRY_SERVER }}:4873
    npm login
