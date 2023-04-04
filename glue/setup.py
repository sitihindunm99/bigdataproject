from setuptools import setup

# to create whl package for external python libraries
setup(
    name="glue_python_shell_module",
    version="4.2.0",
    install_requires=[
        "gensim"
    ]
)