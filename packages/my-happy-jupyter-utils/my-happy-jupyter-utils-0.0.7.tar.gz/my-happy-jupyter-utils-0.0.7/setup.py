import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

install_requires = [
            'requests>=2.24.0'
        ]


from my_happy_jupyter_utils import version

setup(
  name="my-happy-jupyter-utils",
  version=version.get_current(),
  description="Jupyter utils",
  long_description=README,
  long_description_content_type="text/markdown",
  license="Apache 2",
  url="https://github.com/ggservice007/my-happy-jupyter-utils",
  author="ggservice007",
  author_email="ggservice007@126.com",
  packages=find_packages(exclude=[""]),
  install_requires=install_requires,
  include_package_data=True,
  zip_safe=False,
  python_requires=">=3.7.7"
)
