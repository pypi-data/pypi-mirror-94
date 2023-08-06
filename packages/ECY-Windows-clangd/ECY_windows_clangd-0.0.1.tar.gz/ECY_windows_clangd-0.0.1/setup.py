from os import path
from platform import system
from setuptools import Extension, setup

# with open(path.join(path.dirname(__file__), "README.md")) as f:
#     LONG_DESCRIPTION = f.read()

LONG_DESCRIPTION = "Clone from https://github.com/clangd/clangd/releases/tag/11.0.0 for Windows OS."

setup(name="ECY_windows_clangd",
      version="0.0.1",
      maintainer="jimmy huang",
      maintainer_email="1902161621@qq.com",
      author="jimmy huang",
      author_email="1902161621@qq.com",
      url="https://github.com/clangd/clangd/releases/tag/11.0.0",
      license="MIT",
      platforms=["any"],
      python_requires=">=3.3",
      description="Python bindings to the Tree-sitter parsing library",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Topic :: Software Development :: Compilers",
          "Topic :: Text Processing :: Linguistic",
      ],
      packages=["ECY_windows_clangd"])
