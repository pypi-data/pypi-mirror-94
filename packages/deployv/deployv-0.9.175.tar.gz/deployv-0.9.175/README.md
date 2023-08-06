CI Status
===

[![Pypi version](https://img.shields.io/pypi/v/deployv.svg)](https://pypi.python.org/pypi/deployv)
[![Build status](https://git.vauxoo.com/vauxoo/deployv/badges/master/build.svg)](https://git.vauxoo.com/vauxoo/deployv/commits/master)
[![coverage status](https://git.vauxoo.com/vauxoo/deployv/badges/master/coverage.svg)](https://coverage.vauxoo.com/master-master/)
[![Documentation](https://git.vauxoo.com/vauxoo/deployv/badges/master/build.svg)](https://git.vauxoo.com/deployv/orchest/wikis/home)

DeployV
===

The main DeployV goal is to have a set of tools for working with dockerized Odoo instances as a library or command line
interface using a simple json formatted config files.

It is planned that in further versions will be an [Odoo](https://www.odoo.com) integration so the whole configuration
process can be done directly in the instance and deployed to the corresponding server (this would be configurable too)
using [RabbitMQ](https://www.rabbitmq.com/) for messaging. This graphical interface development is done in 
the [Orchest](https://github.com/Vauxoo/orchest) repository.


Getting started
===

## Installing

Before installing the library you will need to have the following installed:

* build-essential
* python-setuptools
* python-dev
* libpq-dev
* libffi-dev

This can be performed executing the following:

    $ sudo apt-get update 
    $ sudo apt-get install build-essential python-setuptools python-dev libpq-dev libffi-dev

All Python dependencies are listed in the requirements.txt and will be installed when you run:
    
    $ python setup.py install
    
Notice that you must have docker and PostgreSQL installed on your system, if not you can install docker following the
[official documentation](https://docs.docker.com/installation/ubuntulinux) and you can use the a PostgreSQL container 
([vauxoo/docker-postgresql](https://hub.docker.com/r/vauxoo/docker-postgresql/)), run it:

    $ docker run -d -p 127.0.0.1:5136:5432 -p 172.17.42.1:5136:5432 --name odoo_psql vauxoo/docker-postgresql:latest /entry_point.py
    
The port 5136 is used to avoid conflict with any postgres running instance. It is attached to the docker interface and
the [loopback](http://www.tldp.org/LDP/nag/node66.html) so it is accessible from the container and the host only,
the **--name** parameter is optional and can be changed to your needs. To see a detailed description of the parameters
go to [docker cli documentation page](https://docs.docker.com/reference/commandline/cli/).

**Note:** This have been tested with docker 1.7.1 only

## Testing the installation

In the test folder you can find a sample configuration file names *config.json* this file uses a 
[docker test image](https://hub.docker.com/r/vauxoo/odoo80-test/) that have some public repositories and Odoo 8.0.

Run the create command:

    $ deployvcmd create -f /path/to/tests/config.json -l DEBUG -z /any/path
    
Notice that the backup must start with customer_id if you specify a directory, if you specify a specific file only then
the name format does not matter.

## Basic commands

The image for the instance can be created by:

    $ deployvcmd build -u git@github.com:user/app_repo.git -v 8.0

And it will create a docker image using Odoo 8.0 and will install all dependencies from the requirements.txt and oca_dependencies.txt, if you wish to build from
a development branch just do:

    $ deployvcmd build -u git@github.com:user-dev/app_repo.git -b my_dev_branch -v 8.0  
   
As you can see in the test section you can easily create an Odoo instance using the command line, but also generate
a backup from it:

    $ deployvcmd backupdb -f /path/to/tests/config.json -z ./backup/path -d database_name_to_backup
    
Or you can create a backup from an instance in a container:

    $ deployvcmd backupdb -n container_name -z ./backup/path -d database_name_to_backup

I will generate a compressed file in *./backup/path* with a database dump, attachments and a json file with the
instance branches info.

To restore the generated dump just have to execute:

    $ deployvcmd restore -f /path/to/tests/config.json -z ./backup/path

Also, if you want to restore it to a dockerized instance:

    $ deployvcmd restore -n container_name -z ./backup/path

This will search the best best backup to restore or if you wish to specify one:

    $  deployvcmd restore -f /path/to/tests/config.json -z ./backup/path/backup_file.tar.bz2

The database name is generated automatically, but you can change this behaviour too:

    $ deployvcmd restore -f /path/to/tests/config.json -z ./backup/path/backup_file.tar.bz2 -d specific_database_name


 
