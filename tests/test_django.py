import pytest
from goodconf import GoodConf
from goodconf.contrib.django import execute_from_command_line_with_config

pytest.importorskip('django')


def test_mgmt_command(mocker, tmpdir):
    mocked_load_config = mocker.patch('goodconf._load_config')
    mocked_dj_execute = mocker.patch(
        'django.core.management.execute_from_command_line')
    temp_config = tmpdir.join('config.yml')
    temp_config.write('')
    c = GoodConf()
    dj_args = ['manage.py', 'diffsettings', '-v', '2']
    c.django_manage(dj_args + ['-C', str(temp_config)])
    mocked_load_config.assert_called_once_with(str(temp_config))
    mocked_dj_execute.assert_called_once_with(dj_args)


def test_help(mocker, tmpdir, capsys):
    mocker.patch('sys.exit')
    mocked_load_config = mocker.patch('goodconf._load_config')
    temp_config = tmpdir.join('config.yml')
    temp_config.write('')
    c = GoodConf(
        file_env_var='MYAPP_CONF',
        default_files=['/etc/myapp.json'])
    assert c.file_env_var == 'MYAPP_CONF'
    c.django_manage([
        'manage.py', 'diffsettings', '-C', str(temp_config),
        '--settings', __name__, '-h'])
    mocked_load_config.assert_called_once_with(str(temp_config))
    output = capsys.readouterr()
    assert '-C FILE, --config FILE' in output.out
    assert 'MYAPP_CONF' in output.out
    assert '/etc/myapp.json' in output.out


# This doubles as a Django settings file for the tests
SECRET_KEY = 'abc'
