
# PyTorch CUDA Installer

PyTorch CUDA Installer is a Python package that simplifies the process of installing PyTorch packages with CUDA support. It automatically detects the available CUDA version on your system and installs the appropriate PyTorch packages.

## Installation

You can install the PyTorch CUDA Installer using pip:

```
pip install torch-cuda-installer
```

## Usage

After installation, you can use the package in two ways:

1. As a command-line tool:

   ```
   torch-cuda-installer --torch --torchvision --torchaudio
   ```

2. As a Python module:

   ```python
   from torch_cuda_installer import install_pytorch

   install_pytorch(cuda_key=None, packages=['torch', 'torchvision', 'torchaudio'])
   ```

Use any combination of `--torch`, `--torchvision`, and `--torchaudio` to select which packages to install.
