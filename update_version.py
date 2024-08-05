import os
import re
import subprocess

def update_version(new_version):
    # Update __init__.py
    init_path = os.path.join('torch_cuda_installer', '__init__.py')
    with open(init_path, 'r') as f:
        content = f.read()
    content = re.sub(r'__version__\s*=\s*"[\d.]+"', f'__version__ = "{new_version}"', content)
    with open(init_path, 'w') as f:
        f.write(content)

    # Update pyproject.toml
    pyproject_path = 'pyproject.toml'
    with open(pyproject_path, 'r') as f:
        content = f.read()
    content = re.sub(r'version\s*=\s*"[\d.]+"', f'version = "{new_version}"', content)
    with open(pyproject_path, 'w') as f:
        f.write(content)

    print(f"Updated version to {new_version}")

    # Reinstall the package
    subprocess.run(["pip", "install", "-e", "."], check=True)
    print("Reinstalled package")

if __name__ == "__main__":
    new_version = input("Enter the new version number: ")
    update_version(new_version)