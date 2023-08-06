# Koha synchronizer #

Este modulo permite sincronizar registros de Koha al sistema estadistico Lookproxy. 

### Instalacion

Para instalar el modulo `koha-sync` debe seguir estos pasos:

##### **Requerimientos**
* python 3.7+
* El servidor desde el cual ejecuta el modulo, debe tener conexion con el servidor Koha
* La instalacion la puede realizar en un `host dedicado` o en un `host compartido`
  * **host dedicado**: significa que el modulo se ejecuta en un servidor exclusivamente para este proceso. El servidor 
  puede ser de 512 MB o 1 GB de RAM.  
  * **host compartido**: significa  que el modulo de ejecuta en el mismo servidor del Koha.
   
##### **Crear directorio raiz**
```sh
> mkdir /opt/koha-sync
``` 

##### **Instalar y crear sesion de tmux**
```sh
> apt-get install tmux
> tmux new -s koha-sync
```
para salirse de la sesion, debe presionar `ctrl + b + d`


##### Instalar Python3.7

* [Ubuntu](https://websiteforstudents.com/installing-the-latest-python-3-7-on-ubuntu-16-04-18-04/)
* [CentOs 8](https://linuxize.com/post/how-to-install-python-on-centos-8/)
* [CentOs 7](https://tecadmin.net/install-python-3-7-on-centos/)

Al finalizar la instalacion, verifique que corresponda a la `3.7`
```sh
> alias python='python3.7'
> python -V
  |_______3.7
```

##### Instalar pip3

* [Ubuntu](https://itsfoss.com/install-pip-ubuntu/)
* [CentOs 8](https://linuxize.com/post/how-to-install-pip-on-centos-8/)
* [CentOs 7](https://linuxize.com/post/how-to-install-pip-on-centos-7/)

Al finalizar la instalacion, verifique que corresponda a la `20+`
```sh
> pip3 -V
  |______pip 20.1 from /usr/local/lib/python3.5/dist-packages/pip (python 3.7)
```

##### Instalar setuptools
```sh
> python3.7 -m pip install setuptools
```

##### Instalar y activar virtaulenv (solo si la instalacion es compartida)
```sh
> python3.7 -m pip install virtualenv
> cd /opt/koha-sync & virtualenv venv
> source /opt/koha-sync/venv/bin/activate
```

##### Instalar el modulo koha-sync
```sh
> python -m pip install koha-sync
```

##### Cargar al servidor el config.yml enviado por Referencistas
```sh
ls
|__ config.yml
```

#### Ejecutar el comando
```yml
koha_syncrhonizer --help

    Options:
     -V, --version           print current cli version and stops execution
     -c, --config-file TEXT  path to configuration file  [required]
     -v, --verbose           activate verbosity output
     -r, --run-once          synchronize once and stops execution
     -t, --test              run validations and stops before synchronize
     --help                  Show this message and exit.

```

**Copyright © [Referencistas](https://www.referencistas.com/)**
