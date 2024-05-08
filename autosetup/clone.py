#!/usr/bin/env python3

'''
Script: clone.py
Description:
    This script clones a list of GitHub repositories using the git command.
    It checks if a repository already exists in the current directory before cloning.
    The repositories to clone are defined in the 'repos' list.
    The repositories will be cloned into the current directory.

Preliminaries:
    - Before running the script, ensure that the necessary dependencies (git, python3) are installed.
Usage:
    Either
        python3 clone.py
        ./clone.py  (Then you have to modify the privileges of the file)

'''

import os
import subprocess

repos = [
            "git@github.com:navikt/arena-rest-facade.git"
        ,   "git@github.com:navikt/brev-administrasjon.git"
        ,   "git@github.com:navikt/brukersok-frontend.git"
        ,   "git@github.com:navikt/forstesidegenerator.git"
        ,   "git@github.com:navikt/gosys-felles-webkomponenter.git"
        ,   "git@github.com:navikt/gosys-tjenestespesifikasjoner.git"
        ,   "git@github.com:navikt/gosys.git"
        ,   "git@github.com:navikt/infotrygd-sak-rest-facade.git"
        ,   "git@github.com:navikt/jfr-arena.git"
        ,   "git@github.com:navikt/jfr-generell.git"
        ,   "git@github.com:navikt/jfr-infotrygd.git"
        ,   "git@github.com:navikt/jfr-manuell.git"
        ,   "git@github.com:navikt/journalforing-frontend.git"
        ,   "git@github.com:navikt/kubeconfigs.git"
        ,   "git@github.com:navikt/notat-administrasjon.git"
        ,   "git@github.com:navikt/personsok-frontend.git"
        ,   "git@github.com:navikt/testdata-frontend.git"
        ]

def clone_repo(repo_url):
    repo_name = repo_url.split("/")[-1].split(".git")[0]
    repo_dir = os.path.join("repos", repo_name)

    if os.path.exists(repo_name):
        print(f"Skipping {repo_name}. Repository already exists.")
    else:
        print(f"Cloning from repo url [{repo_url}]")
        command = ["git", "clone", repo_url, repo_dir]
        result = subprocess.run(command)
        if result.returncode == 0:
            print(f"Cloned {repo_name} successfully.")
        else:
            print(f"Failed to clone {repo_name}.")

os.makedirs("repos", exist_ok=True)
for repo in repos:
    clone_repo(repo)
