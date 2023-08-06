from setuptools import setup, find_packages
from requests import get

setup(
      name='pypi_test_castellani_davide_01_01-castellani-davide',
      version=get("https://api.github.com/repos/CastellaniDavide/pypi_test_castellani_davide_01_01/tags").json()[0]['name'].replace("v", "") if len(get("https://api.github.com/repos/CastellaniDavide/pypi_test_castellani_davide_01_01/tags").json()) > 0 else "0.0", # Lastest release
      description=get("https://api.github.com/repos/CastellaniDavide/pypi_test_castellani_davide_01_01").json()['description'],
      long_description=get("https://raw.githubusercontent.com/CastellaniDavide/pypi_test_castellani_davide_01_01/master/docs/README.md").text,
      long_description_content_type="text/markdown",
      url=get("https://api.github.com/repos/CastellaniDavide/pypi_test_castellani_davide_01_01").json()['html_url'],
      author=get("https://api.github.com/repos/CastellaniDavide/pypi_test_castellani_davide_01_01").json()['owner']['login'],
      author_email=get(f"https://api.github.com/users/{get('https://api.github.com/repos/CastellaniDavide/pypi_test_castellani_davide_01_01').json()['owner']['login']}").json()['email'],
      license='GNU',
      packages=find_packages(),
      python_requires=">=3.7",
      platforms="linux_distibution",
      install_requires=[i for i in get("https://raw.githubusercontent.com/CastellaniDavide/pypi_test_castellani_davide_01_01/master/requirements/requirements.txt").text.split("\n") if not "#" in i and i != ''],
      zip_safe=True
      )
