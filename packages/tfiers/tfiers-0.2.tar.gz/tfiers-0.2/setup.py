from setuptools import find_packages, setup


GITHUB_URL = "https://github.com/tfiers/tfiers-py"

with open("ReadMe.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="tfiers",
    description="My notebook setup and matplotlib style",
    author="Tomas Fiers",
    author_email="tomas.fiers@gmail.com",
    long_description=readme,
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={"Source Code": GITHUB_URL},
    python_requires=">= 3.8",
    install_requires=[
        "preload ~= 2.2",
        "seaborn",
        # "pyjanitor",  # pip installing pyjanitor forces all optional extra deps of
        #                 janitor to be installed (like heavy pyspark etc). No thanks.
        #                 Conda does it right.
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},  # (`""` is the "root" package).
    # Get package version from git tags
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "dirty-tag",
    },
)
