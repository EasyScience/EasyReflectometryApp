import os, sys
import time
import requests
import xml.dom.minidom
import dephell_licenses
import Functions, Config
import Signatures
import datetime


CONFIG = Config.Config()

def qtifwSetupFileName():
    file_version = CONFIG['ci']['qtifw']['version']
    file_name_base = CONFIG['ci']['qtifw']['file_name_base']
    file_platform = CONFIG['ci']['qtifw']['file_platform'][CONFIG.os]
    file_ext = CONFIG['ci']['qtifw']['file_ext'][CONFIG.os]
    return f'{file_name_base}-{file_platform}-{file_version}.{file_ext}'

def qtifwSetupDownloadDest():
    return os.path.join(CONFIG.download_dir, f'{qtifwSetupFileName()}')

def urlOk(url):
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

def qtifwSetupDownloadUrl():
    repos = CONFIG['ci']['qtifw']['https_mirrors']
    base_path = CONFIG['ci']['qtifw']['base_path']
    qtifw_version = CONFIG['ci']['qtifw']['version']
    try:
        message = f'access Qt Installer Framework download url'
        for repo in repos:
            url = f'https://{repo}/{base_path}/{qtifw_version}/{qtifwSetupFileName()}'
            if urlOk(url):
                message += f' {url}'
                break
    except Exception as exception:
        message += f'from any of {repos}'
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)
        return url

def qtifwSetupExe():
    setup_name, _ = os.path.splitext(qtifwSetupFileName())
    d = {
        'macos': f'/Volumes/{setup_name}/{setup_name}.app/Contents/MacOS/{setup_name}',
        'ubuntu': qtifwSetupDownloadDest(),
        'windows': qtifwSetupDownloadDest()
    }
    return d[CONFIG.os]

def qtifwDirPath():
    home_dir = os.path.expanduser('~')
    qtifw_version = CONFIG['ci']['qtifw']['version']
    d = {
        'macos': f'{home_dir}/Qt/QtIFW-{qtifw_version}',
        'ubuntu': f'{home_dir}/Qt/QtIFW-{qtifw_version}',
        'windows': f'C:\\Qt\\QtIFW-{qtifw_version}'
    }
    return d[CONFIG.os]

def setupBuildDirPath():
    setup_build_dir_suffix = CONFIG['ci']['setup']['build_dir_suffix']
    return os.path.join(CONFIG.build_dir, f'{CONFIG.app_name}{setup_build_dir_suffix}')

def configDirPath():
    return os.path.join(setupBuildDirPath(), CONFIG['ci']['setup']['build']['config_dir'])

def configXmlPath():
    return os.path.join(configDirPath(), CONFIG['ci']['setup']['build']['config_xml'])

def packagesDirPath():
    return os.path.join(setupBuildDirPath(), CONFIG['ci']['setup']['build']['packages_dir'])

def localRepositoryDir():
    repository_dir_suffix = CONFIG['ci']['setup']['repository_dir_suffix']
    return os.path.join(f'{CONFIG.app_name}{repository_dir_suffix}', CONFIG.setup_os)

def onlineRepositoryUrl() -> str:
    """
    :return: Url of online repository.
    """
    host = CONFIG['ci']['ftp']['host']
    user = CONFIG['ci']['ftp']['user_repo']
    # repo_subdir = CONFIG['ci']['setup']['ftp']['repo_subdir']
    # return f'https://{prefix}.{host}/{repo_subdir}/{CONFIG.setup_os}'
    return f'ftp://{user}:easyDiffraction123@download.{host}/{CONFIG.setup_os}'

def installerConfigXml():
    try:
        message = f"create {CONFIG['ci']['setup']['build']['config_xml']} content"
        app_url = CONFIG['project']['urls']['homepage']
        maintenance_tool_suffix = CONFIG['ci']['setup']['maintenance_tool_suffix']
        maintenance_tool_name = maintenance_tool_suffix #f'{CONFIG.app_name}{maintenance_tool_suffix}'
        config_control_script = CONFIG['ci']['scripts']['config_control']
        config_style = CONFIG['ci']['scripts']['config_style']
        # https://doc.qt.io/qtinstallerframework/ifw-globalconfig.html
        # /Applications/easyTemplate/MaintenanceTool.app/Contents/MacOS/MaintenanceTool --addRepository http://easyscience.apptimity.com/easyTemplateRepo/official/macOS --updater
        # http://download.qt.io/online/qtsdkrepository/windows_x86/root/qt/
        # https://stackoverflow.com/questions/46455360/workaround-for-qt-installer-framework-not-overwriting-existing-installation/46614107#46614107
        raw_xml = Functions.dict2xml({
            'Installer': {
                'Name': CONFIG.app_name,
                'Version': CONFIG.app_version,
                'Title': CONFIG.app_name,
                'Publisher': CONFIG.app_name,
                'ProductUrl': app_url,
                #'Logo': 'logo.png',
                'WizardStyle': 'Classic', #'Aero',
                'WizardDefaultWidth': 900,
                'WizardDefaultHeight': 600,
                'StyleSheet': config_style,
                'StartMenuDir': CONFIG.app_name,
                'TargetDir': CONFIG.installation_dir_for_qtifw,
                #'CreateLocalRepository': 'true',
                #'SaveDefaultRepositories': 'false',
                #'RepositorySettingsPageVisible': 'false',
                # 'RemoteRepositories': {
                #     'Repository': [
                #         {
                #             'Url': onlineRepositoryUrl(),
                #             'DisplayName': f'{CONFIG.app_name} {CONFIG.setup_os}_{CONFIG.setup_arch} repository',
                #             'Enabled': 1,
                #         }
                #     ]
                # },
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

def appPackageXml():
    try:
        message = f"create app package content"
        release_date = datetime.datetime.strptime(CONFIG['ci']['git']['build_date'], "%d %b %Y").strftime("%Y-%m-%d")
        license_id = CONFIG['project']['license'].replace('-only', '')
        license_name = dephell_licenses.licenses.get_by_id(license_id).name.replace('"', "'")
        requires_root = 'false'
        raw_xml = Functions.dict2xml({
            'Package': {
                'DisplayName': CONFIG.app_name,
                'Description': CONFIG['project']['description'],
                'Version': CONFIG.app_version,
                'ReleaseDate': release_date,
                'Default': 'true',
                #'SortingPriority': 100,
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

def downloadQtInstallerFramework():
    Functions.createDir(CONFIG.download_dir)
    Functions.downloadFile(
        url=qtifwSetupDownloadUrl(),
        destination=qtifwSetupDownloadDest()
    )

def osDependentPreparation():
    message = f'prepare for os {CONFIG.os}'
    if CONFIG.os == 'macos':
        Functions.attachDmg(qtifwSetupDownloadDest())
    elif CONFIG.os == 'ubuntu':
        Functions.run('sudo', 'apt-get', 'install', '-qq', 'libxkbcommon-x11-0')
        Functions.setEnvironmentVariable('QT_QPA_PLATFORM', 'minimal')
        Functions.addReadPermission(qtifwSetupExe())
    else:
        Functions.printNeutralMessage(f'No preparation needed for os {CONFIG.os}')

def installQtInstallerFramework():
    if os.path.exists(qtifwDirPath()):
        Functions.printNeutralMessage(f'QtInstallerFramework was already installed to {qtifwDirPath()}')
        return
    try:
        message = f'install QtInstallerFramework to {qtifwDirPath()}'
        silent_script = os.path.join(CONFIG.scripts_dir, CONFIG['ci']['scripts']['silent_install'])
        Functions.installSilently(
            installer=qtifwSetupExe(),
            silent_script=silent_script
        )
        time.sleep(10)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)

def prepareSignedMaintenanceTool():
    if CONFIG.setup_os != "Windows":
        return
    try:
        message = 'copy and sign MaintenanceTool'
        target_dir = CONFIG['ci']['subdirs']['certificates_path']
        target_file = os.path.join(target_dir, "signedmaintenancetool.exe")
        # copy MaintenanceTool locally
        Functions.copyFile(os.path.join(qtifwDirPath(), "bin", "installerbase.exe" ), target_file)
        Signatures.unzipCerts(zip_pass=sys.argv[2])
        Signatures.sign_windows(file_to_sign=target_file, cert_pass=sys.argv[1])
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)

def createInstallerSourceDir():
    try:
        message = f'create installer source directory {setupBuildDirPath()}'
        # base
        Functions.createDir(setupBuildDirPath())
        # config
        config_control_script_path = os.path.join(CONFIG.scripts_dir, CONFIG['ci']['scripts']['config_control'])
        config_style_path = os.path.join(CONFIG.scripts_dir, CONFIG['ci']['scripts']['config_style'])
        Functions.createDir(configDirPath())
        Functions.createFile(path=configXmlPath(), content=installerConfigXml())
        Functions.copyFile(source=config_control_script_path, destination=configDirPath())
        Functions.copyFile(source=config_style_path, destination=configDirPath())
        # package: app
        app_subdir_path = os.path.join(packagesDirPath(), CONFIG['ci']['setup']['build']['app_package_subdir'])
        app_data_subsubdir_path = os.path.join(app_subdir_path, CONFIG['ci']['setup']['build']['data_subsubdir'])
        app_meta_subsubdir_path = os.path.join(app_subdir_path, CONFIG['ci']['setup']['build']['meta_subsubdir'])
        app_package_xml_path = os.path.join(app_meta_subsubdir_path, CONFIG['ci']['setup']['build']['package_xml'])
        package_install_script_src = os.path.join(CONFIG.scripts_dir, CONFIG['ci']['scripts']['package_install'])
        freezed_app_src = os.path.join(CONFIG.dist_dir, f"{CONFIG.app_name}{CONFIG['ci']['pyinstaller']['dir_suffix'][CONFIG.os]}")
        Functions.createDir(packagesDirPath())
        Functions.createDir(app_subdir_path)
        Functions.createDir(app_data_subsubdir_path)
        Functions.createDir(app_meta_subsubdir_path)
        Functions.createFile(path=app_package_xml_path, content=appPackageXml())
        Functions.copyFile(source=package_install_script_src, destination=app_meta_subsubdir_path)
        Functions.copyFile(source=CONFIG.license_file, destination=app_meta_subsubdir_path)
        Functions.copyFile(source=CONFIG['ci']['setup']['changelog_file'], destination=app_meta_subsubdir_path)
        Functions.moveDir(source=freezed_app_src, destination=app_data_subsubdir_path)
        Functions.copyFile(source=CONFIG.license_file, destination=app_data_subsubdir_path)
        Functions.copyFile(source=CONFIG['ci']['setup']['changelog_file'], destination=app_data_subsubdir_path)
        # TODO: change the handling of failure in all methods in Functions.py so they bubble up exceptions
        # TODO: remove this platform conditional once the above is done
        if CONFIG.os == 'windows':
            Functions.copyFile(source=CONFIG.maintenancetool_file, destination=app_data_subsubdir_path)
        if CONFIG.os == 'windows':
            Functions.copyFile(source=CONFIG.maintenancetool_file, destination=app_data_subsubdir_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)

def createOfflineInstaller():
    try:
        message = 'create installer'
        qtifw_bin_dir_path = os.path.join(qtifwDirPath(), 'bin')
        qtifw_binarycreator_path = os.path.join(qtifw_bin_dir_path, 'binarycreator')
        qtifw_installerbase_path = os.path.join(qtifw_bin_dir_path, 'installerbase')
        setup_exe_path = os.path.join(CONFIG.dist_dir, CONFIG.setup_name)
        Functions.run(
            qtifw_binarycreator_path,
            '--verbose',
            '--offline-only',
            '-c', configXmlPath(),
            '-p', packagesDirPath(),
            '-t', qtifw_installerbase_path,
            setup_exe_path
        )
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)

if __name__ == "__main__":
    downloadQtInstallerFramework()
    osDependentPreparation()
    installQtInstallerFramework()
    prepareSignedMaintenanceTool()
    createInstallerSourceDir()
    createOfflineInstaller()