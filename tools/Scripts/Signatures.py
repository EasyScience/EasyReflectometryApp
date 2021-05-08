import os
import sys
import zipfile
import Config
import Functions


CONFIG = Config.Config()

app_name = CONFIG.app_name
app_url = CONFIG['tool']['poetry']['homepage']
installer_exe_path = os.path.join(CONFIG.dist_dir, CONFIG.setup_full_name)

certificates_dir_path = CONFIG['ci']['project']['subdirs']['certificates_path']
certificate_file_path = CONFIG.certificate_path
certificates_zip_path = CONFIG.certificate_zip_path


def unzipCerts(zip_pass=None):

    if zip_pass is None:
        zip_pass = sys.argv[2]

    print('* Unzip certificates')
    with zipfile.ZipFile(certificates_zip_path) as zf:
        zf.extractall(
            path=certificates_dir_path,
            pwd=bytes(zip_pass, 'utf-8'))


def sign_linux():
    print('* No code signing needed for linux')
    return


def sign_windows(file_to_sign=installer_exe_path, cert_pass=None):
    print('* Code signing for windows')
    if cert_pass is None:
        cert_pass = sys.argv[1]
    # using local signtool, since installing the whole SDK is a total overkill
    # signtool_exe_path = os.path.join('C:', os.sep, 'Program Files (x86)', 'Windows Kits', '10', 'bin', 'x86', 'signtool.exe')
    signtool_exe_path = os.path.join(certificates_dir_path, 'signtool.exe')

    win_certificate_file_path = certificate_file_path + ".pfx"

    print('* Sign code with imported certificate')
    Functions.run(
        signtool_exe_path, 'sign',              # info - https://msdn.microsoft.com/en-us/data/ff551778(v=vs.71)
        '/f', win_certificate_file_path,        # signing certificate in a file
        '/p', cert_pass,                        # password to use when opening a PFX file
        '/d', app_name,                         # description of the signed content
        '/du', app_url,                         # URL for the expanded description of the signed content
        '/t', 'http://timestamp.digicert.com',  # URL to a timestamp server
        '/v',                                   # display the verbose version of operation and warning messages
        '/a',                                   # Select the best signing cert automatically
        file_to_sign)


def sign_macos():
    print('* Code signing on MacOS is disabled.')
    return
    keychain_name = 'codesign.keychain'
    keychain_password = 'password'
    mac_certificate_file_path = certificate_file_path + ".p12"
    identity = 'Developer ID Application: European Spallation Source Eric (W2AG9MPZ43)'

    print('* Create keychain')
    Functions.run(
        'security', 'create-keychain',
        '-p', keychain_password,
        keychain_name)

    print('* Set it to be default keychain')
    Functions.run(
        'security', 'default-keychain',
        '-s', keychain_name)

    print('* List keychains')
    Functions.run(
        'security', 'list-keychains')

    print('* Unlock created keychain')
    Functions.run(
        'security', 'unlock-keychain',
        '-p', keychain_password,
        keychain_name)

    print('* Import certificate to created keychain')
    Functions.run(
        'security', 'import',
        mac_certificate_file_path,
        '-k', keychain_name,
        '-P', certificate_password,
        '-T', '/usr/bin/codesign')

    print('* Show certificates')
    Functions.run(
        'security', 'find-identity',
        '-v')

    print('* Allow codesign to access certificate key from keychain')
    Functions.run(
        'security', 'set-key-partition-list',
        '-S', 'apple-tool:,apple:,codesign:',
        '-s',
        '-k', keychain_password)

    print('* Sign code with imported certificate')
    Functions.run(
        'codesign',
        '--deep',
        '--force',
        '--verbose',
        # --timestamp URL
        '--sign', identity,
        installer_exe_path)


if __name__ == "__main__":
    unzipCerts()
    if CONFIG.os == 'ubuntu':
        sign_linux()
    elif CONFIG.os == 'windows':
        sign_windows()
    elif CONFIG.os == 'macos':
        sign_macos()
    else:
        raise AttributeError("Incorrect OS")
