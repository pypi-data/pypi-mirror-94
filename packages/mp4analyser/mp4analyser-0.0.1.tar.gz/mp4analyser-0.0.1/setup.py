import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

dir_loc = os.path.dirname(__file__)
mp4analyser_src_dir = os.path.join(dir_loc, 'mp4analyser', 'mp4analyser')
py_modules = []
for fn in os.listdir(mp4analyser_src_dir):
    name, ext = os.path.splitext(fn)
    if ext == '.py' and not name.startswith('_'):
        py_modules.append('mp4analyser.{}'.format(name))

setuptools.setup(
    name="mp4analyser", # Replace with your own username
    version="0.0.1",
    author="Ziyue \"Alan\" Xiang",
    author_email="ziyue.alan.xiang@gmail.com",
    description="PyPI mirror for essential61/mp4analyser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xziyue/mp4analyser",
    #packages=['mp4analyser'],
    py_modules = py_modules,
    package_dir = {'' : 'mp4analyser'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)