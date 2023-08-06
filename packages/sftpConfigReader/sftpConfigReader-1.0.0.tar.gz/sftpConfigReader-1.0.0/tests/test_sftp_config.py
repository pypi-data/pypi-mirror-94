import pytest
from sftpConfigReader.reader import read_sftp_config, SFTPConfigFileNotFound, SFTPConfigSectionNotFound


@pytest.fixture()
def config_file_path(tmpdir):
    conf_file = tmpdir.mkdir("appconf").join("config.ini")
    content = """    
        [sftp]
        host=sftp.example.com
        port=22
        user=some_name
        password=some_password
        known_hosts=known_hosts_file_location
    """
    conf_file.write(content)
    return str(conf_file)


@pytest.fixture()
def fake_config_file_path():
    return "fake_config.ini"


@pytest.fixture()
def config_section():
    return "sftp"

@pytest.fixture()
def fake_config_section():
    return "fake"


@pytest.fixture()
def expected_credentials():
    return {
        "host": "sftp.example.com",
        "port": "22",
        "user": "some_name",
        "password": "some_password",
        "known_hosts": "known_hosts_file_location"
    }


def test_read_sftp_config_returns_dict(config_file_path, config_section):
    # GIVEN: a valid configuration file and a valid configuration section name
    # WHEN: read_sftp_config() is called
    # THEN: dictionary is returned

    ftp_credentials = read_sftp_config(config_file_path, config_section)
    assert isinstance(ftp_credentials, dict)


def test_read_sftp_config(config_file_path, config_section, expected_credentials):
    # GIVEN: a configuration file provided in test fixture config_file,
    #        and a configuration section provided in test fixture config_section
    # WHEN: read_sftp_config() is called
    # THEN: dictionary equal to the dictionary provided in test fixture expected_credentials returned

    sftp_credentials = read_sftp_config(config_file_path, config_section)
    assert sftp_credentials == expected_credentials


def test_read_sftp_config_conf_file_not_exists(fake_config_file_path, config_section):
    # GIVEN: configuration file does not exist
    # WHEN: read_sftp_config() is called
    # THEN: SFTPConfigFileNotFound exception is raised
    with pytest.raises(SFTPConfigFileNotFound):
        read_sftp_config(fake_config_file_path, config_section)


def test_read_sftp_config_conf_section_not_exists(config_file_path, fake_config_section):
    # GIVEN: configuration section does not exist
    # WHEN: read_sftp_config() is called
    # THEN: SFTPConfigException is raised
    with pytest.raises(SFTPConfigSectionNotFound):
        read_sftp_config(config_file_path, config_section)

