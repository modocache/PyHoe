import sys
import re
import platform
import subprocess
from pyhoe.utils.network import internet_connection_available

def virtualenv_available():
    """
    Returnns True if virtualenv is available,
    False otherwise.
    """
    if any(platform.linux_distribution()) or any(platform.mac_ver()):
        try:
            subprocess.check_call(
                "which virtualenv &> /dev/null",
                shell=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    return False

def virtualenvwrapper_available():
    """
    Returns True if virtualenvwrapper is available,
    False otherwise.
    """
    if virtualenv_available():
        try:
            subprocess.check_call(
                "which virtualenvwrapper.sh &> /dev/null",
                shell=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    return False

def mkvirtualenv(name, env_dir=None, packages_to_install=[]):
    """
    Creates a virtualenv with the specified name.
    Returns True if successful, False otherwise.
    """
    if virtualenvwrapper_available():
        path = subprocess.check_output(
            "which virtualenvwrapper.sh",
            shell = True
        ).strip()
        subprocess.call(
            ". %s && mkvirtualenv %s" % (path, name),
            shell = True
        )
        if internet_connection_available():
            for p in packages_to_install:
                subprocess.call(
                    ". %s && workon %s && pip install %s" % (path, name, p),
                    shell = True
                )
        else:
            sys.stdout.write(
                "Could not download packages -- no internet connection "
                "detected."
            )
        return True
    elif virtualenv_available() and env_dir is not None:
        subprocess.call("virtualenv %s" % name, shell=True)
        if internet_connection_available():
            for p in packages_to_install:
                subprocess.call(
                    ". %s/%s/bin/activate && pip install %s"
                    % (env_dir, name, p)
                )
        return True
    return False

def check_env_for_package(env, package):
    """
    Checks if a particular package has been installed
    in the specified environment.
    """
    if virtualenvwrapper_available():
        path = subprocess.check_output(
            "which virtualenvwrapper.sh",
            shell = True
        ).strip()
        freeze = subprocess.check_output(
            ". %s && workon %s && pip freeze" % (path, env),
            stderr = subprocess.STDOUT,
            shell = True
        ).lower()
        if re.search(package.lower(), freeze):
            return True
        else:
            return False
    elif virtualenv_available():
        freeze = subprocess.call(
            ". %s/bin/activate && pip freeze" % env,
            stderr = subprocess.STDOUT,
            shell = True
        ).lower()
        if re.search(package.lower(), freeze):
            return True
        else:
            return False
    return False
