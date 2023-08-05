import os

import numpy as np
import setuptools
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webrtc_audio",
    version="0.0.1",
    author="Spokestack",
    author_email="support@spokestack.io",
    description="Cython Bindings for WebRTC Audio Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spokestack/webrtc-audio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    setup_requires=["setuptools", "numpy", "Cython"],
    install_requires=[
        "numpy",
        "Cython",
    ],
    ext_modules=cythonize("webrtc_audio/hello.pyx"),
    include_dirs=[np.get_include()],
    zip_safe=False,
)
