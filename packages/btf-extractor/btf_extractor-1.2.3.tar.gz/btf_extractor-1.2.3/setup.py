# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['btf_extractor']

package_data = \
{'': ['*'], 'btf_extractor': ['c_ext/*']}

install_requires = \
['Pillow>=7', 'nptyping>=1,<2', 'numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'btf-extractor',
    'version': '1.2.3',
    'description': 'Extract UBO BTF archive format(UBO2003, UBO2014).',
    'long_description': '# BTF Extractor\n[![PyPI version](https://img.shields.io/pypi/v/btf-extractor?style=flat-square)](https://pypi.org/project/btf-extractor/#history)\n[![GitHub version](https://img.shields.io/github/v/tag/2-propanol/BTF_extractor?style=flat-square)](https://github.com/2-propanol/BTF_extractor/releases)\n[![Python Versions](https://img.shields.io/pypi/pyversions/btf-extractor?style=flat-square)](https://pypi.org/project/btf-extractor/)\n\nExtract UBO BTF archive format([UBO2003](https://cg.cs.uni-bonn.de/en/projects/btfdbb/download/ubo2003/), [UBO2014](https://cg.cs.uni-bonn.de/en/projects/btfdbb/download/ubo2014/)).\n\nThis repository uses [zeroeffects/btf](https://github.com/zeroeffects/btf)\'s [btf.hh](https://github.com/zeroeffects/btf/blob/master/btf.hh).\n\nExtract to ndarray compatible with openCV(BGR, channels-last).\n\n## Install\n```bash\npip install btf-extractor\n```\n\nThis package uses the [Python C API](https://docs.python.org/3/c-api/index.html).\nTo install this package, a C++ build environment is required.\n\n### Build is tested on\n- Windows 10 20H2 + MSVC v14.28 ([Build Tools for Visual Studio 2019](https://visualstudio.microsoft.com/downloads/))\n- MacOS 11(Big Sur) + clang 12.0.0 (Command line tools for Xcode (`xcode-select --install`))\n- Ubuntu 20.04 + GCC 9.3.0 ([build-essential](https://packages.ubuntu.com/focal/build-essential))\n\n## Example\n```python\n>>> from btf_extractor import Ubo2003, Ubo2014\n\n>>> btf = Ubo2003("UBO_CORDUROY256.zip")\n>>> angles_list = list(btf.angles_set)\n>>> image = btf.angles_to_image(*angles_list[0])\n>>> print(image.shape)\n(256, 256, 3)\n>>> print(angles_list[0])\n(0, 0, 0, 0)\n\n>>> btf = Ubo2014("carpet01_resampled_W400xH400_L151xV151.btf")\n>>> print(btf.img_shape)\n(400, 400, 3)\n>>> angles_list = list(btf.angles_set)\n>>> image = btf.angles_to_image(*angles_list[0])\n>>> print(image.shape)\n(400, 400, 3)\n>>> print(angles_list[0])\n(60.0, 270.0, 60.0, 135.0)\n```\n\n## Supported Datasets\n### UBO2003\n6561 images, 256x256 resolution, 81 view and 81 light directions. \n\n![ubo2003](https://user-images.githubusercontent.com/42978570/107014489-02f65c80-67df-11eb-9efc-b0e33670f311.jpg)\n> Mirko Sattler, Ralf Sarlette and Reinhard Klein "[Efficient and Realistic Visualization of Cloth](http://cg.cs.uni-bonn.de/de/publikationen/paper-details/sattler-2003-efficient/)", EGSR 2003.\n\n### ATRIUM (non-HDR)\n6561 images, 800x800 resolution, 81 view and 81 light directions.\n\n![atrium](https://user-images.githubusercontent.com/42978570/107017968-32a76380-67e3-11eb-9e87-a14708182f80.jpg)\n\n### UBO2014\n22,801 images, 512x512(400x400) resolution, 151 view and 151 light directions.\n\n![ubo2014](https://user-images.githubusercontent.com/42978570/107017983-376c1780-67e3-11eb-8416-047b648f64ca.jpg)\n> [Michael Weinmann](https://cg.cs.uni-bonn.de/en/people/dr-michael-weinmann/), [Juergen Gall](http://www.iai.uni-bonn.de/~gall/) and [Reinhard Klein](https://cg.cs.uni-bonn.de/en/people/prof-dr-reinhard-klein/). "[Material Classification based on Training Data Synthesized Using a BTF Database](https://cg.cs.uni-bonn.de/de/publikationen/paper-details/weinmann-2014-materialclassification/)", accepted at ECCV 2014.\n',
    'author': '2-propanol',
    'author_email': 'nuclear.fusion.247@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2-propanol/btf_extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
