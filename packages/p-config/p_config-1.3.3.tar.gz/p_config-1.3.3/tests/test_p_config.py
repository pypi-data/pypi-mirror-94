import os
import pytest

from p_config import Config, Converter

base_dir = os.path.dirname(os.path.abspath(__file__))


def test_default():
    config_file = os.path.join(base_dir, 'default.yml')
    config = Config(config_file, none_exist_key='value', hostnames=None)
    assert config['none_exist_key'] == 'value'
    assert config['server.port'] == 80
    assert config['server.hostname'] == 'localhost'
    assert config['dbs.mysql.hostname'] == 'localhost'
    assert config['dbs.mysql.port'] == 3306
    assert config['dbs.mysql.options.charset'] == 'utf8mb4'
    assert config['hostnames'] == ['demo.com']
    assert config['nodes'] == ['127.0.0.2', '127.0.0.3']
    # test upper case
    assert config['DBS.MYSQL.OPTIONS.CHARSET'] == 'utf8mb4'
    # test title case
    assert config['Dbs.Mysql.Options.Charset'] == 'utf8mb4'

    with pytest.raises(KeyError):
        config['server.unknow']

    assert config.get('Dbs.Mysql.Options.Charset') == 'utf8mb4'
    assert config.get('Dbs.Mysql.Options.None') is None
    assert config.get('Dbs.Mysql.Options.None', 'default') == 'default'
    assert config.get('None', 'default') == 'default'


def test_override_yaml():
    config = Config(os.path.join(base_dir, 'default.yml'))
    config.load(os.path.join(base_dir, 'override.yml'))

    assert config['server.port'] == 8080
    assert config['server.hostname'] == 'localhost'
    assert config['dbs.mysql.hostname'] == 'online.com'
    assert config['dbs.mysql.port'] == 3308
    assert config['dbs.mysql.options.charset'] == 'utf8'
    assert config['dbs.mysql.options.timeout'] == 1000
    assert config['dbs.postgresql.hostname'] == 'online.com'
    assert config['dbs.postgresql.username'] == 'root'
    assert config['nodes.node1'] == '127.0.0.1'
    assert config['nodes'] == {'NODE1': '127.0.0.1'}

    assert config.NODES.NODE1 == '127.0.0.1'
    assert config.NODES == {'NODE1': '127.0.0.1'}

    config['server.port'] = 9090
    assert config['server.port'] == 9090
    assert config['SERVER.PORT'] == 9090
    assert config.SERVER.PORT == 9090


def test_environ():
    config = Config()
    config.set_cast_func('server.port', int)

    os.environ['server.port'] = '22'
    os.environ['SERVER.hostname'] = 'demo.com'

    config.load_env()
    assert config['server.port'] == 22
    assert config['server.hostname'] == 'demo.com'

    os.environ['SERVER.PORT'] = '33'
    config.load_env()
    assert config['server.port'] == 33


def test_attribute():
    config_file = os.path.join(base_dir, 'default.yml')
    config = Config(config_file, none_exist_key='value', hostnames=None)

    assert config.NONE_EXIST_KEY == 'value'
    assert config.SERVER.PORT == 80
    assert config.SERVER.HOSTNAME == 'localhost'

    with pytest.raises(KeyError):
        config.SERVER.UNKNOWN


def test_convterter():
    class Csv(Converter):
        def __call__(self, value):
            return value.split(',')

    class MyConfig(Config):
        port = int
        hosts = Csv()

    config = MyConfig(
        port='22',
        another_port='22',
        hosts='a.com,b.com,c.com',
    )
    assert config.PORT == 22
    assert config.ANOTHER_PORT == '22'
    assert config.HOSTS == ['a.com', 'b.com', 'c.com']
