
import pytest
from torch_cuda_installer import get_cuda_key, get_latest_cuda_version

def test_get_cuda_key():
    cuda_key = get_cuda_key()
    assert cuda_key is None or cuda_key.startswith('cu')

def test_get_latest_cuda_version():
    latest_cuda = get_latest_cuda_version()
    assert latest_cuda.startswith('cu')
    assert len(latest_cuda) == 5  # Should be in format 'cuXXX'
