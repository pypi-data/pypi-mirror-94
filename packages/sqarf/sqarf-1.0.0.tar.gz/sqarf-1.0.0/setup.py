import os

from setuptools import setup, find_packages
import versioneer

readme = os.path.normpath(os.path.join(__file__, "..", "README.md"))
with open(readme, "r") as fh:
    long_description = fh.read()


setup(
    cmdclass=versioneer.get_cmdclass(),
    name="sqarf",
    version=versioneer.get_version(),
    description=("Simple Quality Assurance Reports and Fixes"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/kabaretstudio/sqarf",
    author='Damien "dee" Coureau',
    author_email="dee909@gmail.com",
    license="LGPLv3+",
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # "Development Status :: 3 - Alpha",
        "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        # 'Topic :: System :: Shells',
        "Intended Audience :: Developers",
        # 'Intended Audience :: End Users/Desktop',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    keywords="kabaret blender b3d pipeline dataflow workflow",
    install_requires=[],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'flake8', 'black'],
    },
    # python_requires=">=3.7",
    packages=find_packages("src"),
    package_dir={"": "src"},
)
