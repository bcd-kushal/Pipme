# pipme

pipme is a tool that simplifies the process of publishing Python projects to PyPI. It automates the process of packaging and uploading projects, making it easy for developers to share their Python packages with the world.

## Features

- **Easy publishing**: Publish Python projects to PyPI with a single command.
- **Seamless integration**: Secure and reliable package uploads.
- **Automatic packaging**: Automatically creates distribution packages from your project files.
- **Simple usage**: Just provide your PyPI access token, and pipme takes care of the rest.

## Usage

To use pipme, simply install it via pip:

```bash
pip install pipme
```

Then, navigate to your project root directory and run the following command to publish your project to PyPI:

```bash
pipme
```

- creates new package folder with your project code inside it
- adds `__init__.py` files to every directory as a necessary step
- checks if such pip package already exists or not
- creates `dist_wheel` to create the build folder
- uploads to pip after requesting `access_token` from user
