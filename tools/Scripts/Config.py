# SPDX-FileCopyrightText: 2022 EasyReflectometry contributors
# <support@easyreflectometry.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2022 Contributors to the EasyReflectometry project
# <https://github.com/easyScience/EasyReflectometryApp>

__author__ = ["github.com/AndrewSazonov", "github.com/arm61"]
__version__ = '0.0.1'

import os
import pathlib
import Functions


class Config():

    def __init__(self, branch_name=None):
        # Main
        self.__dict__ = Functions.config()
        self.os = Functions.osName()
        self.branch_name = branch_name

        # Application
        self.app_version = self.__dict__['tool']['poetry']['version']
        self.app_name = self.__dict__['release']['app_name']
        self.family_name = self.__dict__['release']['family_name']
        self.app_file_ext = self.__dict__['ci']['app']['setup']['file_ext'][self.os]
        self.app_full_name = f'{self.app_name}{self.app_file_ext}'

        # Project
        self.package_name = self.__dict__['tool']['poetry']['name']
        self.license_file = self.__dict__['ci']['project']['license_file']
        
        # Directories
        self.scripts_dir = os.path.normpath(
            self.__dict__['ci']['project']['subdirs']['scripts'])
        self.build_dir = os.path.normpath(
            self.__dict__['ci']['project']['subdirs']['build'])
        self.dist_dir = os.path.normpath(
            self.__dict__['ci']['project']['subdirs']['distribution'])
        self.download_dir = os.path.normpath(
            self.__dict__['ci']['project']['subdirs']['download'])
        self.screenshots_dir = os.path.normpath(
            self.__dict__['ci']['project']['subdirs']['screenshots'])
        self.tutorials_dir = os.path.normpath(
            self.__dict__['ci']['project']['subdirs']['tutorials'])
        self.installation_dir = self.installationDir()
        self.installation_dir_for_qtifw = self.installationDirForQtifw()

        # Application setup
        self.setup_os = self.__dict__['ci']['app']['setup']['os'][self.os]
        self.setup_arch = self.__dict__['ci']['app']['setup']['arch'][self.os]
        self.setup_name_suffix = f'_{self.setup_os}_{self.setup_arch}_v{self.app_version}'
        self.setup_name = f'{self.app_name}{self.setup_name_suffix}'
        self.setup_file_ext = self.__dict__['ci']['app']['setup']['file_ext'][self.os]
        self.setup_full_name = f'{self.setup_name}{self.setup_file_ext}'
        self.setup_exe_path = os.path.join(self.dist_dir, self.setup_full_name)

        # Artifacts
        self.setup_zip_path_short = self.setupZipPathShort()
        self.setup_zip_path = self.setupZipPath()
        self.video_tutorial_path = self.videoTutorialPath()

        # Application repository
        self.repository_dir_suffix = self.__dict__['ci']['app']['setup'][
            'repository_dir_suffix']

    def __getitem__(self, key):
        return self.__dict__[key]

    # https://doc.qt.io/qtinstallerframework/scripting.html
    def installationDir(self):
        dirs = {
            'macos': {
                '@HomeDir@': str(pathlib.Path.home()),
                '@ApplicationsDir@': '/Applications',
                '@ApplicationsDirUser@': str(pathlib.Path.home().joinpath('Applications'))
            },
            'ubuntu': {
                '@HomeDir@': str(pathlib.Path.home()),
                '@ApplicationsDir@': '/opt'
            },
            'windows': {
                '@HomeDir@': str(pathlib.Path.home()),
                '@ApplicationsDir@': os.getenv('ProgramFiles'),
                '@ApplicationsDirX86@': os.getenv('ProgramFiles(x86)')
            }
        }
        dir_shortcut = self.__dict__['ci']['app']['setup']['installation_dir_shortcut'][self.os]
        dir = os.path.join(dirs[self.os][dir_shortcut], self.package_name)
        return dir

    def installationDirForQtifw(self):
        dir_shortcut = self.__dict__['ci']['app']['setup']['installation_dir_shortcut'][self.os]
        if self.os == 'macos' and dir_shortcut == '@ApplicationsDir@':
            dir_shortcut = '/Applications'  # @ApplicationsDir@ = @ApplicationsDirUser@ [BUG in QTIFW?]
        dir = os.path.join(dir_shortcut, self.package_name)
        return dir

    def artifactsFileSuffix(self):
        if self.branch_name != 'master' and self.branch_name is not None:
            return f'_{self.branch_name}'
        return ''

    def setupZipPathShort(self):
        setup_zip_name = f'{self.setup_name}.zip'
        setup_zip_path = os.path.join(self.dist_dir, setup_zip_name)
        return setup_zip_path

    def setupZipPath(self):
        file_suffix = self.artifactsFileSuffix()
        setup_zip_name = f'{self.setup_name}{file_suffix}.zip'
        setup_zip_path = os.path.join(self.dist_dir, setup_zip_name)
        return setup_zip_path

    def videoTutorialPath(self):
        file_suffix = self.artifactsFileSuffix()
        video_tutorial_name = f'tutorial_{self.setup_name}{file_suffix}.mp4'
        video_tutorial_path = os.path.join(self.dist_dir, video_tutorial_name)
        return video_tutorial_path


if __name__ == "__main__":
    Config()
