# Development workflow

All development in `EasyReflectometryApp` is done on the `develop` branch of the git repository. 
It is advised that this branch will have the most up to date version of `EasyReflectometryApp`. 
However, this may include bugs so for production use the [latest release](https://github.com/easyScience/EasyReflectometryApp/releases) is advised. 

Development installation instructions are given in the [installation documentation](./INSTALLATION.md).

## Feature/Bug fix contributions

**Note that some features may require contribution to both `EasyReflectometryApp` and [`EasyReflectometryLib`](https://github.com/easyScience/EasyReflectometryLib/).**
If you are interested in contributing a feature or bug fix to `EasyReflectometryApp`, then please fork the Github repository and clone this fork to your local machine and add the upstream repo. 

```
git clone git@github.com:<your-github-username>/EasyReflectometryApp.git
git remote add upstream https://github.com/easyScience/EasyReflectometryApp.git
```

With the repository cloned, change to the `develop` branch

```
git checkout -b develop origin/develop
```

From this branch, you should create a feature branch to make the changes/contributions. 

```
git branch my-feature-branch
git checkout my-feature-branch
```

Once you have completed the feature and commited your changes, please open a pull request to the original `EasyReflectometryApp` repository and wait for a review. 

## Release workflow

Periodically, or after the additional of major new features, there will be stable releases of `EasyReflectometryApp`. 
These should be produced firstly by:
1. Bumping the version number in the `develop` branch appropriately and updating the [CHANGELOG.md](./CHANGELOG.md). 
    The files where the version numbers should be changed are: 
    - `pyproject.toml`
    - `README.md`
    - `INSTALLATION.md`

    This should be allowed to build on Github and the resulting application tested. 
2. Then a branch should be taken from `develop` for the release candidate, named `<version-number>rc`. If there has been changes to `EasyReflectometryLib:main`, the `pyproject.toml` should be changed to use the `main` branch rather than `develop` of `EasyReflectometryLib`. Then a lock file for the poetry package management should be produced and commited to the repository using

    ```
    poetry lock
    git add -f poetry.lock pyproject.toml
    git commit -m 'Lock package versions'
    ```

3. Once the `<version-number>rc` Github builds have been completed, these should also be tested. 
4. Then a pull request can be opened to merge the `<version-number>rc` branch into the `main` branch and tested, at this stage the CHANGELOG.md information for the given release should be copy-and-pasted into the PR.
5. Once this pull request is merged, the final version will be built from `main` and the `<version-number>rc` branch can be removed (locally).
6. The final `main` branch action will then run to build the release version of EasyReflectometry, this will produce a release in the [releases](https://github.com/easyScience/EasyReflectometryApp/releases) section of the Github repository. 
7. Once is it there, the release should be tagged and renamed, this is achieved by selecting the 'edit' button (the pencil). The tag should be given as `v<version-number>` and the name of the release should be `Version <version-number> (<date>)` and currently (until new tutorials are produced) the tutorial should be removed from the release.
8. Finally, the release should be published.  