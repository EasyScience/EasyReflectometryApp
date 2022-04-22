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
These should be produced firstly by bumping the version number in the `develop` branch appropriately and updating the [CHANGELOG.md](./CHANGELOG.md). 
The files where the version numbers should be changed are: 
- `pyproject.toml`
- `README.md`
- `INSTALLATION.md`
Once the version number is bumped and the resulting build EasyReflectometry application is tested, a branch should be taken from `develop` for the release candidate.
This branch should be named `<version-number>rc` and a lock file for the poetry package management should be produced and commited to the repository using

```
poetry lock
git add -f package.lock
git commit -m 'Lock package versions'
```

Once the Githib builds have been completed, these should also be tested. 

If all is well, then a pull request can be opened to merge the `<version-number>rc` branch into the `main` branch. 
With this pull request merged the final version will be built from `main` and the `<version-number>rc` branch can be removed. 
The final `main` branch action will then run to build the release version of EasyReflectometry, this will produce a release in the [releases](https://github.com/easyScience/EasyReflectometryApp/releases) section of the Github repository. 
Once is it there, the release should be tagged and renamed, this is achieved by selecting the 'edit' button (the pencil). 
The tag should be given as `v<version-number>` and the name of the release should be "Version <version-number> (<date>)` and currently (until new tutorials are produced) the tutorial should be removed from the release.
Finally, the release should be published.  