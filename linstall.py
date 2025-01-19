import os
import subprocess

class Linstall:
    def __init__(self, repo_url):
        self.repo_url = repo_url

    def fetch_package(self, package_name, proprietary=False):
        if proprietary:
            print("Warning: You are about to fetch a proprietary package. Be careful cause it might be a rootkit")
        package_url = f"{self.repo_url}/{package_name}.tar.gz"
        print(f"Fetching {package_name} from {package_url}...")
        try:
            subprocess.run(['wget', package_url], check=True)
            print(f"Successfully fetched {package_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Error fetching package: {e}")

    def run_script(self, script_path):
        try:
            subprocess.run(['bash', script_path], check=True)
            print(f"Successfully ran {script_path}.")
        except subprocess.CalledProcessError as e:
            print(f"Error running script {script_path}: {e}")

    def install_package(self, package_name, proprietary=False):
        if proprietary:
            print("Warning: You are about to install a proprietary package. Be careful cause it might be a rootkit.")
        package_file = f"{package_name}.tar.gz"
        print(f"Installing {package_name}...")
        try:
            # Extract the package
            subprocess.run(['tar', '-xzf', package_file], check=True)
            # Run the user-defined installation script
            script_path = f'{package_name}/install.sh'
            if os.path.exists(script_path):
                self.run_script(script_path)
            else:
                print(f"No install script found for {package_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing package: {e}")

    def remove_package(self, package_name):
        print(f"Removing {package_name}...")
        try:
            # Run the user-defined uninstallation script
            script_path = f'{package_name}/uninstall.sh'
            if os.path.exists(script_path):
                self.run_script(script_path)
            else:
                print(f"No uninstall script found for {package_name}.")
            # Remove the package directory
            subprocess.run(['rm', '-rf', package_name], check=True)
            print(f"Successfully removed {package_name}.")
        except subprocess.CalledProcessError as e:
            print(f"Error removing package: {e}")

# Now, when fetching or installing a package, you can specify if it's proprietary:
# linstall.fetch_package("example-package", proprietary=True)
# linstall.install_package("example-package", proprietary=True)
