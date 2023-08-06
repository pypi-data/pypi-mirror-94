##########
p_config
##########

Simple project config for Python.

You can read configuration from environ or local file with it.


***************
Install
***************

.. code:: bash

    $: pip install p_config


***************
Usuage
***************


Suppose there are some config files.

.. code:: yaml

    # filename: default.yml
    server:
        port: 80
        hostname: localhost



.. code:: yaml

    # filename: override.yml
    server:
        port: 443
        hostname: localhost
        backends:
          - 127.0.0.1:80


You can read configuration via this way


.. code:: python

    $: env SERVER.PORT=8080 ipython
    Python 3.6.9 (default, Nov  7 2019, 10:44:02)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.\

    In [1]: from p_config import Config

    In [2]: config = Config('default.yml')

    In [3]: config['SERVER.PORT']
    Out[3]: 80

    In [4]: config['SERVER.HOSTNAME']
    Out[4]: 'localhost'

    In [5]: config.load('override.yml')  # update configuration via local file

    In [6]: config['SERVER.PORT']
    Out[6]: 443

    In [7]: config['SERVER.BACKENDS']
    Out[7]: ['127.0.0.1:8080']

    In [8]: config.load_env()  # update configuration via environ

    In [9]: config['SERVER.PORT']
    Out[9]: '8080'

    In [10]: config.get('SERVER.PORT')
    Out[10]: '8080'

    In [11]: config.get('NONE_EXIST')
    Out[11]: None
