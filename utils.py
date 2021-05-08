import os
import sys
import pip
import pathlib
import datetime
import argparse

try:
    import toml
except ImportError:
    import pip
    pip.main(['install', 'toml'])
    import toml


### Get value from pyproject.toml

def conf():
    project_fname = 'pyproject.toml'
    current_path = os.path.dirname(__file__)
    project_fpath = os.path.join(current_path, project_fname)
    return toml.load(project_fpath)

def keyPath():
    if len(sys.argv) < 2:
        return ''
    return sys.argv[1]

def getValue(d, element):
    keys = element.split('.')
    keys[-1] = keys[-1].split('-')[0] # macos-latest -> macos, etc.
    rv = d
    for key in keys:
        rv = rv[key]
    return rv

### Update pyproject.toml

def extraDict():
    python_packages_path = os.path.dirname(pip.__path__[0]).replace('\\', '/')

    build_date = datetime.datetime.now().strftime('%d %b %Y')

    github_server_url = os.getenv('GITHUB_SERVER_URL', '')
    github_repo = os.getenv('GITHUB_REPOSITORY', '')
    github_repo_url = f'{github_server_url}/{github_repo}'

    branch_name = os.getenv('BRANCH_NAME', '')
    branch_url = f'{github_repo_url}/tree/{branch_name}'

    commit_sha = os.getenv('GITHUB_SHA', '')
    commit_sha_short = commit_sha[:6]
    commit_url = f'{github_repo_url}/commit/{commit_sha}'

    return { 'ci': { 'cache': { 'python_packages_path': python_packages_path },
                     'app': { 'info': { 'build_date': build_date,
                                        'branch_name': branch_name,
                                        'branch_url': branch_url,
                                        'commit_sha_short': commit_sha_short,
                                        'commit_url': commit_url } } } }

def extraToml():
    return toml.dumps(extraDict())

def updatePyprojectToml():
    with open('pyproject.toml', 'r', encoding='utf-8') as f:
        pyproject_toml = f.read()
    pyproject_toml += '\n' + extraToml()
    with open('pyproject.toml', 'w', encoding='utf-8') as f:
        f.write(pyproject_toml)

### Main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--get', dest='key', type=str, help='get parameter value by key from pyproject.toml')
    parser.add_argument('-u', '--update', action='store_true', help='add extra info to the pyproject.toml')
    args = parser.parse_args()
    if args.key:
        value = getValue(conf(), args.key)
        print(value)
    if args.update:
        updatePyprojectToml()

if __name__ == '__main__':
    main()
