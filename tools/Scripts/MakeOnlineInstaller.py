import os, sys
import Functions, Config
from MakeInstaller import qtifwDirPath, localRepositoryDir, packagesDirPath


CONFIG = Config.Config()

def createOnlineRepositoryLocally():
    """
    Uses QtInstaller to create an online repository, for performing
    online updates, and stores this locally. 
    """
    try:
        message = 'create online repository'
        qtifw_bin_dir_path = os.path.join(qtifwDirPath(), 'bin')
        qtifw_repogen_path = os.path.join(qtifw_bin_dir_path, 'repogen')
        repository_dir_path = os.path.join(CONFIG.dist_dir, localRepositoryDir())
        Functions.run(
            qtifw_repogen_path,
            '--verbose',
            '--update-new-components',
            '-p', packagesDirPath(),
            repository_dir_path
        )
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)

def addFilesToLocalRepository():
    """
    Any additional files are added to the local repository. 
    Currently, this is only the CHANGELOG.md
    """
    try:
        message = 'add files to local repository'
        repository_dir_path = os.path.join(CONFIG.dist_dir, localRepositoryDir())
        Functions.copyFile(source=CONFIG['ci']['setup']['changelog_file'], destination=repository_dir_path)
    except Exception as exception:
        Functions.printFailMessage(message, exception)
        sys.exit(1)
    else:
        Functions.printSuccessMessage(message)


if __name__ == "__main__":
    createOnlineRepositoryLocally()
    addFilesToLocalRepository()