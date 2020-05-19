## Resources
A home for any relevant files that don't really fit anywhere else.

### Pipenv & Virtual Environments
This project uses Pipenv for creating and using virtual environments. More info can be at https://pipenv.pypa.io/en/latest/, but the general usage procedure is:

#### Install Pipenv

```Shell
$ pip install pipenv
```

#### Create your virtual environment
Navigate to your project directory and run pipenv install to create the virtual environment for the project.

```bash
$ cd /path/to/repo/social_distancing
$ pipenv install
```

If there is a Pipfile & Pipfile.lock in the directory, it will create the virtual environment and then install the necessary packages.
Otherwise it will create a new empty Pipfile.

#### Install a packages

```bash
$ pipenv install package_name
```

Pipenv will install the package and any dependencies.

#### Running scripts in the virtual environment
Running your scripts from within the virtual environment can be done two ways:

```bash
$ pipenv run python your_script.py

# ==== or ==== #

$ pipenv shell
Launching subshell in virtual environment…
...
$ python your_script.py
...
...
$ exit  # to get out of the virtual environment shell
```

#### Problems
If there seems to be problems with the environment, you can delete it and then rebuild it again using the Pipfile.
To delete the virtual environment (note, this will *not* delete the local Pipfile), run:

```bash
$ pipenv --rm
```
