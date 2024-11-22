from setuptools import setup, find_packages

setup(
    name="amakuru",
    version="0.12",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pdfkit",
        "jinja2",
        "selenium",
        "wkhtmltopdf",
        "sqlalchemy",
        "psycopg2",
        "python-dotenv",
        "setuptools",
        "wheel",
        "twine",
    ],
    entry_points={
        "console_scripts": [
            "amakuru=start:main",
        ],
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Michael Nwuju",
    author_email="michaelnwuju213@gmail.com",
    description="A simple menu-driven application for tech career roadmaps for women.",
    url="https://github.com/michael-alu/amakuru",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
