__version__ = '0.3.0rc1'
git_version = '09cab356336162d99f822cd6e934e47ee1fa229a'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
