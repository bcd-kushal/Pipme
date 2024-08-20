# Pipme: Package bundler to PyPI 

<img style="width:24px" title="python3" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png"/> &nbsp;
<img style="width:24px" title="linux" src="https://github.com/marwin1991/profile-technology-icons/assets/76662862/2481dc48-be6b-4ebb-9e8c-3b957efe69fa"/> &nbsp;
<img style="width:24px" title="windows" src="https://user-images.githubusercontent.com/25181517/186884150-05e9ff6d-340e-4802-9533-2c3f02363ee3.png"/> &nbsp;
<img style="width:24px" title="macOS" src="https://user-images.githubusercontent.com/25181517/186884152-ae609cca-8cf1-4175-8d60-1ce1fa078ca2.png"/> &nbsp;

pipme is a tool that simplifies the process of publishing Python projects to PyPI. It automates the process of packaging and uploading projects, making it easy for developers to share their Python packages with the world.

```bash
pip install pipme
```

<hr />

## ✨ Features

- **Easy publishing**: Publish Python projects to PyPI with a single command.
- **Seamless integration**: Secure and reliable package uploads.
- **Automatic packaging**: Automatically creates distribution packages from your project files.
- **Simple usage**: Just provide your PyPI access token, and pipme takes care of the rest.

<hr />

## 🌻 Usage

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

<hr />

## 🤝 Contributions

Contributions are welcome! 

If you have ideas for improvements, new features, or bug fixes, please feel free to open an issue or submit a pull request.

## ⚖️ License

This project is licensed under the MIT License - see the <a href=''>LICENSE</a> file for details.

<hr>

<h3><img title="Kushal-Kumar" width="18" src="https://raw.githubusercontent.com/bcd-kushal/bcd-kushal/main/assets/icons/dark/filled/kushalkumar_bg_dark.png"/>&nbsp;Kushal Kumar 2024 • All rights reserved </h3>
