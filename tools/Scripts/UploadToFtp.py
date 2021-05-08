__author__ = "github.com/AndrewSazonov"
__version__ = '0.0.1'

import os, sys
import ftplib
import pathlib
import Functions, Config


CONFIG = Config.Config()

def connect(ftp, host, port):
    try:
        message = f'connect to ftp server'
        ftp.connect(host, port)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def login(ftp, user, password):
    try:
        message = f'login to ftp server'
        ftp.login(user, password)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def winToLin(path):
    return path.replace('\\', '/')

def makeDir(ftp, path):
    try:
        message = f'make directory {path}'
        ftp.mkd(path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def uploadFile(ftp, source, destination):
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
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def uploadDir(ftp, source, destination):
    try:
        message = f'upload dir {source} to {destination}'
        root_dir_name = os.path.basename(source)
        for dir_path, _, file_names in os.walk(source):
            for file_name in file_names:
                source_file = os.path.join(dir_path, file_name)
                parent_path = os.path.relpath(source_file, source)
                parent_dir = os.path.dirname(parent_path)
                destination_dir = os.path.join(destination, root_dir_name, parent_dir).rstrip(os.path.sep)
                uploadFile(ftp, source_file, destination_dir)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def upload(ftp, source, destination):
    try:
        message = f'upload {source} to {destination}'
        if os.path.isfile(source):
            uploadFile(ftp, source, destination)
        elif os.path.isdir(source):
            uploadDir(ftp, source, destination)
        else:
            Functions.printFailMessage(message)
            sys.exit()
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def removeDir(ftp, path):
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
        if ftp.nlst(path):
            ftp.rmd(path)
        else:
            Functions.printNeutralMessage(f"Skip next step: Remove directory {path}. It doesn't exist")
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)

def deploy():
    branch = sys.argv[1]
    #if branch != 'master':
    #    Functions.printNeutralMessage(f'No deploy needed for branch {branch}')
    #    return

    password = sys.argv[2]
    host = CONFIG['ci']['app']['setup']['ftp']['host']
    port = CONFIG['ci']['app']['setup']['ftp']['port']
    user = CONFIG['ci']['app']['setup']['ftp']['user']
    remote_subdir_name = CONFIG['ci']['app']['setup']['ftp']['remote_subdir']

    local_repository_dir_name = f'{CONFIG.app_name}{CONFIG.repository_dir_suffix}'
    local_repository_dir_path = os.path.join(CONFIG.dist_dir, local_repository_dir_name, CONFIG.setup_os)
    remote_repository_dir_path = os.path.join(remote_subdir_name, CONFIG.setup_os)

    ftp = ftplib.FTP()
    connect(ftp, host, port)
    login(ftp, user, password)
    removeDir(ftp, remote_repository_dir_path)
    upload(ftp, local_repository_dir_path, remote_subdir_name)
    ftp.quit()

if __name__ == "__main__":
    deploy()
