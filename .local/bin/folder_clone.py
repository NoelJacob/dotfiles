import subprocess
import sys


def run(command, folder=None):
    try:
        subprocess.run(command, check=True, shell=True, cwd=folder)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        exit(1)


def append(filename, text):
    with open(filename, 'a') as file:
        file.write(text)


def default(repo_url):
    command = f"git ls-remote --symref {repo_url} HEAD"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error occurred: {error.decode('utf-8')}")
        exit(1)
    return output.decode('utf-8')[16:].split('\t', 1)[0]


def do(url):
    match = url.split('/tree/main/', 1)
    git = match[0]
    full_folder = match[1]
    folder = git.rsplit('/', 1)[1]
    branch = default(git)
    run(f'git init {folder} -b {branch}')
    run(f'git remote add origin {git}', folder)
    run(f'git config core.sparseCheckout true', folder)
    append(f'{folder}/.git/info/sparse-checkout', full_folder)
    run(f'git pull origin {branch} --depth 1', folder)


do(sys.argv[1])
