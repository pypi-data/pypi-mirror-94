import os
from configparser import ConfigParser


class SFTPConfigException(Exception):
    def __init__(self, message, error=None):
        if error:
            message += "\n\t" + str(error)
        super().__init__(message)


class SFTPConfigFileNotFound(SFTPConfigException):
    pass


class SFTPConfigSectionNotFound(SFTPConfigException):
    pass


def read_sftp_config(conf_file, section='sftp'):
    parser = ConfigParser()
    parser.read(conf_file)

    # check if configuration file exists
    if not os.path.isfile(conf_file):
        raise SFTPConfigFileNotFound(f"Configuration file was not found at:\n\t{conf_file}.")

    if parser.has_section(section):
        sftp_conn_params = parser.items(section)
    else:
        msg = f"Section [{section}] was not found in the configuration file:\n\t{conf_file}"
        raise SFTPConfigSectionNotFound(msg)

    sftp_credentials = {
        'host': sftp_conn_params[0][1],
        'port': sftp_conn_params[1][1],
        'user': sftp_conn_params[2][1],
        'password': sftp_conn_params[3][1],
        'known_hosts': sftp_conn_params[4][1]
    }
    return sftp_credentials
