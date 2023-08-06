import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="napari_pyclesperanto_assistant",
    version="0.7.2",
    author="Robert Haase",
    author_email="robert.haase@tu-dresden.de",
    description="OpenCL based GPU-accelerated image processing in napari",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clesperanto/napari_pyclesperanto_assistant",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["numpy", "pyopencl", "toolz", "scikit-image", "napari==0.4.5", "napari_plugin_engine", "pyclesperanto_prototype==0.7.0", "magicgui==0.2.6", "numpy!=1.19.4", "pyperclip"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: napari",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
    ],
    entry_points={
        'napari.plugin': [
            'clEsperanto = napari_pyclesperanto_assistant',
        ],
    },
)
