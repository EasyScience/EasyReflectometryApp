# SPDX-FileCopyrightText: 2022 EasyReflectometry contributors
# <support@easyreflectometry.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the EasyReflectometry project
# <https://github.com/easyScience/EasyReflectometryApp>

__author__ = ["github.com/AndrewSazonov", "github.com/arm61"]
__version__ = '0.0.1'

import os
import sys
import time
import requests
import xml.dom.minidom
import dephell_licenses
import Functions
import Config

CONFIG = Config.Config()


def qtifwSetupFileName() -> str:
    """
    :return: File name path for the Qt Installer Framework.
    """
    file_version = CONFIG['ci']['qtifw']['setup']['version']
    file_name_base = CONFIG['ci']['qtifw']['setup']['file_name_base']
    file_platform = CONFIG['ci']['qtifw']['setup']['file_platform'][CONFIG.os]
    file_ext = CONFIG['ci']['qtifw']['setup']['file_ext'][CONFIG.os]
    return f'{file_name_base}-{file_platform}-{file_version}.{file_ext}'


def qtifwSetupDownloadDest() -> str:
    """
    :return: Download destination for the Qt Installer Framework.
    """
    return os.path.join(CONFIG.download_dir, f'{qtifwSetupFileName()}')


def urlOk(url) -> bool:
    """
    :return: If the url is accessable.
    """
    try:
        message = f'access url {url}'
        status_code = requests.head(url, timeout=10).status_code
        if status_code == 200:
            Functions.printSuccessMessage(message)
            return True
        else:
            message += f' with status: {status_code}'
            Functions.printFailMessage(message)
            return False
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        return False


def qtifwSetupDownloadUrl() -> str:
    """
    :return: Download url for the Qt Installer Framework.
    """
    repos = CONFIG['ci']['qtifw']['setup']['https_mirrors']
    base_path = CONFIG['ci']['qtifw']['setup']['base_path']
    qtifw_version = CONFIG['ci']['qtifw']['setup']['version']
    try:
        message = 'access Qt Installer Framework download url'
        for repo in repos:
            url = f'https://{repo}/{base_path}/{qtifw_version}/{qtifwSetupFileName()}'
            if urlOk(url):
                message += f' {url}'
                break
    except Exception as exception:
        message += f'from any of {repos}'
        Functions.printFailMessage(message, exception)
        sys.exit()
    else:
        Functions.printSuccessMessage(message)
        return url


def qtifwSetupExe() -> str:
    """
    :return: Location of the Qt Installer Framework installer.
    """
    setup_name, _ = os.path.splitext(qtifwSetupFileName())
    print(qtifwSetupFileName())
    print(os.path.exists(qtifwSetupFileName()))
    d = {
        'macos': f'/Volumes/{setup_name}/{setup_name}.app/Contents/MacOS/{setup_name}',
        'ubuntu': qtifwSetupDownloadDest(),
        'windows': qtifwSetupDownloadDest()
    }
    return d[CONFIG.os]


def qtifwDirPath() -> str:
    """
    :return: Installation location for the Qt Installer Framework.
    """
    home_dir = os.path.expanduser('~')
    qtifw_version = CONFIG['ci']['qtifw']['setup']['version']
    d = {
        'macos': f'{home_dir}/Qt/QtIFW-{qtifw_version}',
        'ubuntu': f'{home_dir}/Qt/QtIFW-{qtifw_version}',
        'windows': f'C:\\Qt\\QtIFW-{qtifw_version}'
    }
    return d[CONFIG.os]


def setupBuildDirPath() -> str:
    """
    :return: Build location for application.
    """
    setup_build_dir_suffix = CONFIG['ci']['app']['setup']['build_dir_suffix']
    return os.path.join(CONFIG.build_dir, f'{CONFIG.app_name}{setup_build_dir_suffix}')


def configDirPath() -> str:
    """
    :return: Path for config directory.
    """
    return os.path.join(setupBuildDirPath(),
                        CONFIG['ci']['app']['setup']['build']['config_dir'])


def configXmlPath() -> str:
    """
    :return: Path for config xml file.
    """
    return os.path.join(configDirPath(),
                        CONFIG['ci']['app']['setup']['build']['config_xml'])


def packagesDirPath() -> str:
    """
    :return: Path for packages directory.
    """
    return os.path.join(setupBuildDirPath(),
                        CONFIG['ci']['app']['setup']['build']['packages_dir'])


def localRepositoryDir() -> str:
    """
    :return: Location of the local repository.
    """
    repository_dir_suffix = CONFIG['ci']['app']['setup']['repository_dir_suffix']
    return os.path.join(f'{CONFIG.app_name}{repository_dir_suffix}', CONFIG.setup_os)


def onlineRepositoryUrl() -> str:
    """
    :return: Url of online repository.
    """
    # host = CONFIG['ci']['app']['setup']['ftp']['host']
    # prefix = CONFIG['ci']['app']['setup']['ftp']['prefix']
    # repo_subdir = CONFIG['ci']['app']['setup']['ftp']['repo_subdir']
    # return f'https://{prefix}.{host}/{repo_subdir}/{CONFIG.setup_os}'
    return 'ftp://u652432322.easyreflectometry_repo:easyDiffraction123@download.' + \
        f'easydiffraction.org/{CONFIG.setup_os}'


def installerConfigXml() -> str:
    """
    :return: Installer configration as an xml string.
    """
    try:
        message = "create ' + \
            f'{CONFIG['ci']['app']['setup']['build']['config_xml']} content"
        app_url = CONFIG['tool']['poetry']['homepage']
        maintenance_tool_name = CONFIG['ci']['app']['setup']['maintenance_tool_suffix']
        config_control_script = CONFIG['ci']['scripts']['config_control']
        config_style = CONFIG['ci']['scripts']['config_style']
        raw_xml = Functions.dict2xml({
            'Installer': {
                'Name': CONFIG.app_name,
                'Version': CONFIG.app_version,
                'Title': CONFIG.app_name,
                'Publisher': CONFIG.app_name,
                'ProductUrl': app_url,
                'WizardStyle': 'Classic',
                'WizardDefaultWidth': 900,
                'WizardDefaultHeight': 600,
                'StyleSheet': config_style,
                'StartMenuDir': CONFIG.family_name,
                'TargetDir': CONFIG.installation_dir_for_qtifw,
                'RemoteRepositories': {
                    'Repository': [{
                        'Url': onlineRepositoryUrl(),
                        'DisplayName':
                        f'{CONFIG.app_name} ' +
                        f'{CONFIG.setup_os}_{CONFIG.setup_arch} repository',
                        'Enabled': 1,
                    }]
                },
                'MaintenanceToolName': maintenance_tool_name,
                'AllowNonAsciiCharacters': 'true',
                'AllowSpaceInPath': 'true',
                'InstallActionColumnVisible': 'false',
                'ControlScript': config_control_script,
            }
        })
        pretty_xml = xml.dom.minidom.parseString(raw_xml).toprettyxml()
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)
        return pretty_xml


def appPackageXml() -> str:
    """
    :return: Application package description as an xml string.
    """
    try:
        message = "create app package content"
        license_id = CONFIG['tool']['poetry']['license'].replace('-only', '')
        license_name = dephell_licenses.licenses.get_by_id(license_id).name.replace(
            '"', "'")
        raw_xml = Functions.dict2xml({
            'Package': {
                'DisplayName': CONFIG.app_name,
                'Description': CONFIG['tool']['poetry']['description'],
                'Version': CONFIG.app_version,
                'ReleaseDate': CONFIG['ci']['app']['info']['date_for_qtifw'],
                'Default': 'true',
                'Essential': 'true',
                'ForcedInstallation': 'true',
                'RequiresAdminRights': 'false',
                'Licenses': {
                    'License': {
                        '@name': license_name,
                        '@file': CONFIG.license_file
                    }
                },
                'Script': CONFIG['ci']['scripts']['package_install'],
            }
        })
        pretty_xml = xml.dom.minidom.parseString(raw_xml).toprettyxml()
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)
        return pretty_xml


# def docsPackageXml():
#    try:
#        message = f"create docs package content"
#        name = CONFIG['ci']['app']['setup']['build']['docs_package_name']
#        description = CONFIG['ci']['app']['setup']['build']['docs_package_description']
#        version = CONFIG['ci']['app']['setup']['build']['docs_package_version']
#        release_date = "2020-01-01"
#        raw_xml = Functions.dict2xml({
#            'Package': {
#                'DisplayName': f'{name} {version}',
#                'Description': description,
#                'Version': version,
#                'ReleaseDate': release_date,
#                'Default': 'true',
#                'SortingPriority': 20,
#            }
#        })
#        pretty_xml = xml.dom.minidom.parseString(raw_xml).toprettyxml()
#    except Exception as exception:
#        Functions.printFailMessage(message, exception)
#        sys.exit()
#    else:
#        Functions.printSuccessMessage(message)
#        return pretty_xml


def downloadQtInstallerFramework():
    """
    Download Qt Installer Framework.
    """
    Functions.createDir(CONFIG.download_dir)
    Functions.downloadFile(url=qtifwSetupDownloadUrl(),
                           destination=qtifwSetupDownloadDest())


def osDependentPreparation():
    """
    Prepare for the Qt Installer Framework installation dependent on the OS.
    """
    if CONFIG.os == 'macos':
        Functions.attachDmg(qtifwSetupDownloadDest())
    elif CONFIG.os == 'ubuntu':
        Functions.run('sudo', 'apt-get', 'install', '-qq', 'libxkbcommon-x11-0')
        Functions.setEnvironmentVariable('QT_QPA_PLATFORM', 'minimal')
        Functions.addReadPermission(qtifwSetupExe())
    else:
        Functions.printNeutralMessage(f'No preparation needed for os {CONFIG.os}')


def installQtInstallerFramework():
    """
    Install the Qt Installer Framework.
    """
    if os.path.exists(qtifwDirPath()):
        Functions.printNeutralMessage(
            f'QtInstallerFramework was already installed to {qtifwDirPath()}')
        return
    try:
        print("Step 1")
        message = f'install QtInstallerFramework to {qtifwDirPath()}'
        print("Step 2")
        silent_script = os.path.join(CONFIG.scripts_dir,
                                     CONFIG['ci']['scripts']['silent_install'])
        print("Step 3")
        Functions.installSilently(installer=qtifwSetupExe(),
                                  silent_script=silent_script)
        print("Step 4")
        time.sleep(10)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def createInstallerSourceDir():
    """
    Create the installer source directory.
    """
    try:
        message = f'create installer source directory {setupBuildDirPath()}'
        # base
        Functions.createDir(setupBuildDirPath())
        # config
        config_control_script_path = os.path.join(
            CONFIG.scripts_dir, CONFIG['ci']['scripts']['config_control'])
        config_style_path = os.path.join(CONFIG.scripts_dir,
                                         CONFIG['ci']['scripts']['config_style'])
        Functions.createDir(configDirPath())
        Functions.createFile(path=configXmlPath(), content=installerConfigXml())
        Functions.copyFile(source=config_control_script_path,
                           destination=configDirPath())
        Functions.copyFile(source=config_style_path, destination=configDirPath())
        # package: app
        app_subdir_path = os.path.join(
            packagesDirPath(),
            CONFIG['ci']['app']['setup']['build']['app_package_subdir'])
        app_data_subsubdir_path = os.path.join(
            app_subdir_path, CONFIG['ci']['app']['setup']['build']['data_subsubdir'])
        app_meta_subsubdir_path = os.path.join(
            app_subdir_path, CONFIG['ci']['app']['setup']['build']['meta_subsubdir'])
        app_package_xml_path = os.path.join(
            app_meta_subsubdir_path,
            CONFIG['ci']['app']['setup']['build']['package_xml'])
        package_install_script_src = os.path.join(
            CONFIG.scripts_dir, CONFIG['ci']['scripts']['package_install'])
        freezed_app_src = os.path.join(
            CONFIG.dist_dir,
            f"{CONFIG.app_name}{CONFIG['ci']['pyinstaller']['dir_suffix'][CONFIG.os]}")
        Functions.createDir(packagesDirPath())
        Functions.createDir(app_subdir_path)
        Functions.createDir(app_data_subsubdir_path)
        Functions.createDir(app_meta_subsubdir_path)
        Functions.createFile(path=app_package_xml_path, content=appPackageXml())
        Functions.copyFile(source=package_install_script_src,
                           destination=app_meta_subsubdir_path)
        Functions.copyFile(source=CONFIG.license_file,
                           destination=app_meta_subsubdir_path)
        Functions.copyFile(source=CONFIG['release']['changelog_file'],
                           destination=app_meta_subsubdir_path)
        Functions.moveDir(source=freezed_app_src, destination=app_data_subsubdir_path)
        Functions.copyFile(source=CONFIG.license_file,
                           destination=app_data_subsubdir_path)
        Functions.copyFile(source=CONFIG['release']['changelog_file'],
                           destination=app_data_subsubdir_path)
        # package: docs
        # # docs_subdir_path = os.path.join(packagesDirPath(),
        # #     CONFIG['ci']['app']['setup']['build']['docs_package_subdir'])
        # # docs_data_subsubdir_path = os.path.join(docs_subdir_path,
        # #     CONFIG['ci']['app']['setup']['build']['data_subsubdir'])
        # # docs_meta_subsubdir_path = os.path.join(docs_subdir_path,
        # #     CONFIG['ci']['app']['setup']['build']['meta_subsubdir'])
        # # docs_package_xml_path = os.path.join(docs_meta_subsubdir_path,
        # #     CONFIG['ci']['app']['setup']['build']['package_xml'])
        # docs_dir_src = CONFIG['ci']['project']['subdirs']['docs']['src']
        # docs_dir_dest = CONFIG['ci']['project']['subdirs']['docs']['dest']
        # # Functions.createDir(docs_subdir_path)
        # # Functions.createDir(docs_data_subsubdir_path)
        # # Functions.createDir(docs_meta_subsubdir_path)
        # # Functions.createFile(path=docs_package_xml_path, content=docsPackageXml())
        # # Functions.copyDir(source=docs_dir_src,
        # #     destination=os.path.join(docs_data_subsubdir_path, 'Documentation'))
        # # Functions.copyDir(source=docs_dir_src,
        # #     destination=os.path.join(app_data_subsubdir_path, docs_dir_dest))
        # package: examples
        # examples_dir_src = CONFIG['ci']['project']['subdirs']['examples']['src']
        # examples_dir_dest = CONFIG['ci']['project']['subdirs']['examples']['dest']
        # Functions.copyDir(source=examples_dir_src,
        #     destination=os.path.join(app_data_subsubdir_path, examples_dir_dest))
        # TODO: change the handling of failure in all methods in
        # Functions.py so they bubble up exceptions
        # TODO: remove this platform conditional once the above is done
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def createOfflineInstaller():
    """
    Create the offline installer.
    """
    try:
        message = 'create offline installer'
        qtifw_bin_dir_path = os.path.join(qtifwDirPath(), 'bin')
        qtifw_binarycreator_path = os.path.join(qtifw_bin_dir_path, 'binarycreator')
        qtifw_installerbase_path = os.path.join(qtifw_bin_dir_path, 'installerbase')
        setup_exe_path = os.path.join(CONFIG.dist_dir, CONFIG.setup_name)
        Functions.run(qtifw_binarycreator_path, '--verbose', '--offline-only', '-c',
                      configXmlPath(), '-p', packagesDirPath(), '-t',
                      qtifw_installerbase_path, setup_exe_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def createOnlineRepositoryLocally():
    """
    Locally build the online repository.
    """
    try:
        message = 'create online repository'
        qtifw_bin_dir_path = os.path.join(qtifwDirPath(), 'bin')
        qtifw_repogen_path = os.path.join(qtifw_bin_dir_path, 'repogen')
        repository_dir_path = os.path.join(CONFIG.dist_dir, localRepositoryDir())
        Functions.run(qtifw_repogen_path, '--verbose', '--update-new-components', '-p',
                      packagesDirPath(), repository_dir_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


def addFilesToLocalRepository():
    """
    Add necessary files to the local repository.
    """
    try:
        message = 'add files to local repository'
        repository_dir_path = os.path.join(CONFIG.dist_dir, localRepositoryDir())
        Functions.copyFile(source=CONFIG['release']['changelog_file'],
                           destination=repository_dir_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    downloadQtInstallerFramework()
    osDependentPreparation()
    installQtInstallerFramework()
    createInstallerSourceDir()
    createOfflineInstaller()
    createOnlineRepositoryLocally()
    addFilesToLocalRepository()
