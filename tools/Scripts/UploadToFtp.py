# SPDX-FileCopyrightText: 2022 EasyReflectometry contributors
# <support@easyreflectometry.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the EasyReflectometry project
# <https://github.com/easyScience/EasyReflectometryApp>

__author__ = ["github.com/AndrewSazonov", "github.com/arm61"]
__version__ = '0.0.1'

import os
import sys
import ftplib
import Functions
import Config

CONFIG = Config.Config()


def connect(ftp: ftplib.FTP, host: str, port: str):
    """
    Connect to the ftp server.

    :param ftp: FTP object to interact with.
    :param host: Host address.
    :param port: Access port.
    """
    try:
        message = 'connect to ftp server'
        ftp.connect(host, port)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def login(ftp: ftplib.FTP, user: str, password: str):
    """
    ftp server login.

    :param ftp: FTP object to interact with.
    :param user: Username.
    :param password: Password.
    """
    try:
        message = 'login to ftp server'
        ftp.login(user, password)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def winToLin(path) -> str:
    """
    Convert from windows paths to unix.

    :param path: Input windows-format path.
    :return: Output unix-format path.
    """
    return path.replace('\\', '/')


def makeDir(ftp: ftplib.FTP, path: str):
    """
    Make a directory on the ftp server.

    :param ftp: FTP object to interact with.
    :param path: Path for new directory.
    """
    if pathExists(ftp, path):
        Functions.printNeutralMessage(f'Directory exists: {path}')
        return
    try:
        path = winToLin(path)
        message = f'create directory {path}'
        ftp.mkd(path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def uploadFile(ftp: ftplib.FTP, source: str, destination: str):
    """
    :param ftp: FTP object to interact with.
    :param source: Path to file to be uploaded.
    :param destination: Path to be uploaded to.
    """
    try:
        destination = winToLin(destination)
        message = f'upload file {source} to {destination}'
        dir_name = os.path.basename(destination)
        dir_names = ftp.nlst(os.path.dirname(destination))
        if dir_name not in dir_names:
            makeDir(ftp, destination)
        destination = f'{destination}/{os.path.basename(source)}'
        with open(source, 'rb') as fb:
            ftp.storbinary(f'STOR {destination}', fb)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def uploadDir(ftp: ftplib.FTP, source: str, destination: str):
    """
    :param ftp: FTP object to interact with.
    :param source: Path to directory to be uploaded.
    :param destination: Path to be uploaded to.
    """
    try:
        message = f'upload dir {source} to {destination}'
        root_dir_name = os.path.basename(source)
        for dir_path, _, file_names in os.walk(source):
            for file_name in file_names:
                source_file = os.path.join(dir_path, file_name)
                parent_path = os.path.relpath(source_file, source)
                parent_dir = os.path.dirname(parent_path)
                destination_dir = os.path.join(destination, root_dir_name,
                                               parent_dir).rstrip(os.path.sep)
                uploadFile(ftp, source_file, destination_dir)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def upload(ftp: ftplib.FTP, source: str, destination: str):
    """
    :param ftp: FTP object to interact with.
    :param source: Path to be uploaded.
    :param destination: Path to be uploaded to.
    """
    try:
        message = f'upload {source} to {destination}'
        if os.path.isfile(source):
            uploadFile(ftp, source, destination)
        elif os.path.isdir(source):
            uploadDir(ftp, source, destination)
        else:
            Functions.printFailMessage(message)
            sys.exit(1)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def pathExists(ftp: ftplib.FTP, path: str) -> bool:
    """
    :param ftp: FTP object to interact with.
    :param source: Path to be determined if it exists.
    :return: If the path does exist.
    """
    try:
        message = f'find path {path}'
        ftp.nlst(path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        return False
    else:
        Functions.printSuccessMessage(message)
        return True


def removeDir(ftp: ftplib.FTP, path: str):
    """
    :param ftp: FTP object to interact with.
    :param source: Path for directory to be removed.
    """
    if not pathExists(ftp, path):
        Functions.printNeutralMessage(f"Directory doesn't exists: {path}")
        return
    try:
        path = winToLin(path)
        message = f'remove directory {path}'
        for (name, properties) in ftp.mlsd(path=path):
            if name in ['.', '..']:
                continue
            elif properties['type'] == 'file':
                ftp.delete(f'{path}/{name}')
            elif properties['type'] == 'dir':
                removeDir(ftp, f'{path}/{name}')
        ftp.rmd(path)
    except Exception as exception:
        Functions.printNeutralMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def deploy():
    """
    Deploy the repository to the ftp server.
    """
    branch = sys.argv[1]
    if branch != 'master':
        Functions.printNeutralMessage(f'No ftp upload for branch {branch}')
        return

    password = sys.argv[2]
    host = CONFIG['ci']['app']['setup']['ftp']['host']
    port = CONFIG['ci']['app']['setup']['ftp']['port']
    user = CONFIG['ci']['app']['setup']['ftp']['user']
    prefix = CONFIG['ci']['app']['setup']['ftp']['prefix']
    repo_subdir = CONFIG['ci']['app']['setup']['ftp']['repo_subdir']

    local_repository_dir_name = f'{CONFIG.app_name}{CONFIG.repository_dir_suffix}'
    local_repository_dir_path = os.path.join(CONFIG.dist_dir, local_repository_dir_name,
                                             CONFIG.setup_os)
    online_repository_subdir_path = f'{prefix}/{repo_subdir}'
    online_repository_dir_path = f'{online_repository_subdir_path}/{CONFIG.setup_os}'

    ftp = ftplib.FTP()
    connect(ftp, host, port)
    login(ftp, user, password)
    removeDir(ftp, online_repository_dir_path)
    makeDir(ftp, online_repository_dir_path)
    upload(ftp, local_repository_dir_path, online_repository_subdir_path)
    ftp.quit()


if __name__ == "__main__":
    deploy()
