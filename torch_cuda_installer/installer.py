import subprocess
import sys
import re
import argparse
import urllib.request
import json

def get_cuda_key():
    try:
        output = subprocess.check_output(["nvidia-smi"]).decode('utf-8')
        match = re.search(r'CUDA Version: (\d+)\.(\d+)', output)
        if match:
            major, minor = match.groups()
            return f'cu{major}{minor}'
        else:
            return None
    except:
        return None

def get_latest_cuda_version():
    try:
        url = "https://download.pytorch.org/whl/torch_stable.html"
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
        cuda_versions = re.findall(r'cu\d+', html)
        return max(cuda_versions, key=lambda x: int(x[2:]))
    except:
        return 'cu118'  # Fallback to a known stable version

def install_pytorch(cuda_key, packages):
    base_command = [sys.executable, "-m", "pip", "install"]

    if cuda_key:
        print(f"Detected CUDA: {cuda_key}")
        latest_cuda = get_latest_cuda_version()
        if cuda_key > latest_cuda:
            print(f"CUDA {cuda_key} is not supported by PyTorch. Falling back to {latest_cuda}")
            cuda_key = latest_cuda
        print(f"Installing PyTorch packages for CUDA {cuda_key}")
        base_command.extend(["--index-url", f"https://download.pytorch.org/whl/{cuda_key}"])
    else:
        print("CUDA not detected. Installing CPU versions of PyTorch packages.")

    base_command.extend(packages)
    try:
        subprocess.check_call(base_command)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during installation: {e}")
        print("Please check your internet connection and try again.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Install PyTorch packages with CUDA support if available.")
    parser.add_argument("--torch", action="store_true", help="Install torch")
    parser.add_argument("--torchvision", action="store_true", help="Install torchvision")
    parser.add_argument("--torchaudio", action="store_true", help="Install torchaudio")
    args = parser.parse_args()

    packages = []
    if args.torch:
        packages.append("torch")
    if args.torchvision:
        packages.append("torchvision")
    if args.torchaudio:
        packages.append("torchaudio")

    if not packages:
        print("No packages selected. Please use --torch, --torchvision, or --torchaudio to select packages.")
        sys.exit(1)

    cuda_key = get_cuda_key()
    install_pytorch(cuda_key, packages)

    print("Verifying installation:")
    verification_commands = []
    if "torch" in packages:
        verification_commands.append(
            "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')")
    if "torchvision" in packages:
        verification_commands.append("import torchvision; print(f'torchvision version: {torchvision.__version__}')")
    if "torchaudio" in packages:
        verification_commands.append("import torchaudio; print(f'torchaudio version: {torchaudio.__version__}')")

    try:
        subprocess.check_call([sys.executable, "-c", "; ".join(verification_commands)])
    except subprocess.CalledProcessError:
        print("Verification failed. The packages may not have installed correctly.")

if __name__ == "__main__":
    main()
