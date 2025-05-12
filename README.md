# NAOqi3

This project introduces a **NAOqi3** - Python 3-compatible wrapper for the NAOqi SDK, originally available only in Python 2. With this bridge, you can write code that communicates with NAO robots in Python 3, using the same syntax as NAOqi's original Python 2 library.

This interface will work with the current library to ensure full functionality of this library with modern versions of Python.

**The main goal of developing this interface is to be able to use the NAOqi library with modern tools** - image processing libraries, AI and ML tools etc. that are in Python version 3 and above.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Compatibility](#compatibility)
3. [Technical Details](#technical-details)
4. [Installation guide](#installation-guide)
   1. [Step 1: Install Python 3 (if not installed)](#step-1-install-python-3-if-not-installed)
   2. [Step 2: Install Python 2.7.18 (required)](#step-2-install-python-2718-required)
   3. [Step 3: Install NAOqi SDK 2.1.4 and add it to Python global dependencies (required)](#step-3-install-naoqi-sdk-214-and-add-it-to-python-global-dependencies-required)
   4. [Step 4: Setup first project and install NAOqi3 (required)](#step-4-setup-first-project-and-install-naoqi3-required)
5. [How to use it?](#how-to-use-it)
6. [Functionality description](#functionality-description)
7. [FAQ](#faq)



## Compatibility
This table shows with which NAO and NAOqi SDK this bridge interface is compatible.
| NAO version | NAOqi SDK version | Compatible |
|-------------|-------------------|------------|
| NAO V4      | *NAOqi* 2.1.4     |     ✅     |
| NAO V5      | *NAOqi* 2.1.4     |     ✅     |
| NAO V6      | *NAOqi* 2.8.6     |     ✅     |


## Technical Details
This project consists of two components:
- **NAOqi3** (code in this repo),
- **NAOqi SDK** (original library that must be installed separately).

The whole project is written in Python 3.11.0 and primarly designed for NAOqi SDK version 2.1.4 (for NAO robots versions 4 and 5).

## Installation guide
**STEPS:**
1. [Python 3.11.0 installation](#step-1-install-python-3-if-not-installed) (or any other versions you would like)
2. [Python 2.7.18 installation](#step-2-install-python-2718-required) (required for NAOqi SDK)
3. [NAOqi SDK instalation](#step-3-install-naoqi-sdk-214-and-add-it-to-python-global-dependencies-required)
4. [Setup first project and install NAOqi3](#step-4-setup-first-project-and-install-naoqi3-required) (TODO: improve this section)

### Step 1: Install Python 3 (if not installed)
_This step is required if you don't have Python 3 installed on your system. If you already have Python 3, you can skip this step._<br>
_In case of any problems, visit [FAQ](#faq) section._ <br>

1. Go to [official Python website](https://www.python.org/downloads/release/python-3110/) to download Python 3.11.0.
2. Scroll to the very end of the page and you will see different installers.
3. Select installer based on your PC system architecture:
   - Windows installer (64-bit) if you have 64-bit system architecture
   - Windows installer (32-bit) if you have 32-bit system architecture
   <img width="1164" alt="python3110_install" src="https://github.com/user-attachments/assets/8c95ae13-5f94-43f9-9da9-ae56f0dd3338" />
   - In this tutorial the 64-bit version will be selected.
4. Click on it to start downloading.
5. After the installation is complete, open the installed file. You should see similar to this window:  
![00_install_python3110](https://github.com/user-attachments/assets/b19cb1f6-7f38-4c38-9593-5c4c9fec6590)  
6. Firstly, select "Add python.exe to PATH" and click "Customize installation"
![02_install_python3110](https://github.com/user-attachments/assets/d88f2c5e-d433-4acb-9f22-876d6f71f59e)  
7. Then check if first two optional features (checkboxes) are selected. Then click "Next"  
![03_install_python3110](https://github.com/user-attachments/assets/49dd439a-6f9c-47c5-83a3-23e8cb524cce)  
8. Select "Install Python for all users" (admin account is required) and check if all options from 2 to 5 are selected.  
Install location can be leaved as default. Click "Install".  
![04_install_python3110](https://github.com/user-attachments/assets/8e69f333-4737-408e-80d7-a378a85e32ce)  
10. Wait for installation to be finished.  
![05_install_python3110](https://github.com/user-attachments/assets/ae6a79be-38f7-408b-a522-b42016ef8f83)  
11. The close installation window.  
![06_install_python3110](https://github.com/user-attachments/assets/68cbd9b9-e73a-48b8-b626-debc1a78c30d)  
12. Check the installation:
   - open CMD console or Windows PowerShell
   - type: `python --version`
   - as an output you should see `Python 3.11.0`

**You have successfully installed Python 3 on your computer!**

### Step 2: Install Python 2.7.18 (required)
_In case of any problems, visit [FAQ](#faq) section._ <br>

1. First, go to this [official link](https://www.python.org/downloads/release/python-2718/) to install exactly Python 2.7.18 32-bit edition.
2. Scroll down and click on this installer: **Windows x86 MSI installer**  
<img width="1168" alt="python2718_installer" src="https://github.com/user-attachments/assets/ecd1e243-e7e9-4e7b-bd51-5900a6602790" />  
3. After the installation is complete, open the installed file. You should see similar to this window.  
<img alt="01_install_python2718" src="https://github.com/user-attachments/assets/04c9ba70-1fef-4307-9388-d4b0027be4ed" />  <br>
4. Select the option: "Install for all users" and click "Next".  <br>
<img alt="02_install_python2718" src="https://github.com/user-attachments/assets/37049bbb-575e-4be4-9d81-a629019d3e89" />  <br>
5. Change installation location, if you want, for example from `C:\Python27` to `C:\Program Files\Python27` and click "Next".  <br>
<img alt="03_install_python2718" src="https://github.com/user-attachments/assets/b1529642-6180-43f6-bbc3-70608a648c39" /> <br>
<img alt="04_install_python2718" src="https://github.com/user-attachments/assets/5434300f-f556-4adb-898f-e2e07d440cec" /> <br>
6. Here hust click "Next".  <br>
<img alt="05_install_python2718" src="https://github.com/user-attachments/assets/dafcde58-b57f-4b49-a85d-29db96f6b409" /> <br>
7. The installation should be started.  <br>
<img alt="06_install_python2718" src="https://github.com/user-attachments/assets/0e507d8f-9815-4797-8d22-dbaa3c64354d" /> <br>
8. Click "Finish" to exit the installation.  <br>
<img alt="07_install_python2718" src="https://github.com/user-attachments/assets/c0e9d248-f346-43a8-8469-6692eb6c79af" /> <br>

**You have successfully installed Python 2.7.18 on your computer!**

### Step 3: install NAOqi SDK 2.1.4 and add it to Python global dependencies (required)
_In case of any problems, visit [FAQ](#faq) section._ <br>

1. Firstlly, install NAOqi SDK from this repository by clicking on this link [pynaoqi.rar](pynaoqi.rar) and clicking on an install icon. <br>
<img width="1096" alt="install_rar" src="https://github.com/user-attachments/assets/04311ba5-5ec0-421d-80df-892bb33b058a" />  <br>
2. After the installation is complete, extract the archive. After the extraction you should see a folder `📁 pynaoqi`.
3. Then copy entire folder `pynaoqi` and place it in folder with the path: `C:\Program Files\Python27\Lib\site-packages`.
4. Next click "Win" button on your keyboard and type "Edit the system environment variables". Then click "Enter".
5. You should see this window opened:  <br>
<img alt="01_install_naoqisdk" src="https://github.com/user-attachments/assets/3e94c685-60bc-4608-a2a1-9fbc92e2cd37" />  <br>
6. Then click on "Environment variables": <br>
<img alt="02_install_naoqisdk" src="https://github.com/user-attachments/assets/fd52181d-f165-407f-941c-9a0b18f1be9e" />  <br>
7. Click on "New": <br>
<img alt="03_install_naoqisdk" src="https://github.com/user-attachments/assets/2bde41f2-e9a5-4677-a6f3-d0eba2535f1f" />  <br>
8. Create new variable with name `PYTHONPATH` and value `your-path-to-python27\Lib\site-packages\pynaoqi\lib` and click "Ok": <br>
<img alt="04_install_naoqisdk" src="https://github.com/user-attachments/assets/10829a62-0cf5-4a16-82a6-39a6b425a835" />  <br>
9. Check if new variable was successfully added and click "Ok".  <br>
<img alt="05_install_naoqisdk" src="https://github.com/user-attachments/assets/9a07adbf-c9ea-4d42-977a-dd695da4cd70" />  <br>
10. Exit by clicking on "Ok".  <br>
<img alt="06_install_naoqisdk" src="https://github.com/user-attachments/assets/f8caa170-b60c-4ed5-8211-fdf3dbdcace5" />  <br>

**You have successfully installed and added NAOqi SDK to your Python 2.7.18 environment!**

### Step 4: Setup first project and install NAOqi3 (required)
_For this part you need to have a git system installed on your computer._ <br>
_Also you need to have a Python IDE installed on your computer (for example VSCode)._ <br>
_In case of any problems, visit [FAQ](#faq) section._ <br>

This part will describe how to create new project in VSCode, clone NAOqi3 from this repository and setup all required settings.

1. Install VSCode (if not installed) following this [official manual](https://code.visualstudio.com/docs/setup/windows#_install-vs-code-on-windows).
2. After successfully installing the VSCode, launch it. <br>
<img alt="01_launch_vscode" width="75%" src="https://github.com/user-attachments/assets/ea7e7845-4e08-4c83-923a-6c8fbc74acf1" />  <br>
3. Create a new project by clicking on "Open folder": <br>
<img alt="02_open_folder_vscode" width="75%" src="https://github.com/user-attachments/assets/909db633-500b-494c-a740-e3976987888d" />  <br>
4. The File Explorer will be opened. Go to any folder you like or create a new one and then click "Select Folder". <br>
<img alt="03_create_folder_vscode" src="https://github.com/user-attachments/assets/9ae51159-9781-4282-9e9a-8fa8ecb5df72" />  <br>
5. You opened an empty VSCode project, then click on the icon that is illustrated on a screenshot to open a terminal: <br>
<img alt="04_open_terminal" width="75%" src="https://github.com/user-attachments/assets/076208ca-160b-4a61-b14d-9191557c42bf" />  <br>
8. Then clone the NAOqi3 from the remote repository by typing this command into the terminal: `git clone https://github.com/KyryloYefremov/My-naoqi-project` as is shown on the screenshot: <br>
<img alt="05_clone_vscode" width="75%" src="https://github.com/user-attachments/assets/0cb47cb2-bee7-4bb0-95ff-9606a68da38c" />  <br>
9. After successful cloning the repository, you will se new folder `My-naoqi-project`.
<img alt="06_cloned_vscode" width="75%" src="https://github.com/user-attachments/assets/5183058d-eb0d-4f99-ba11-e807d8aaefd1" />  <br>
10. Then in the opened terminal navigate to `.\My-naoqi-project\client` folder using this command `cd .\My-naoqi-project\client`. <br>
11. Next create a new virtual environment from Python 3 using a command: `<your-path-to-python3-folder>\python.exe -m venv .venv3` (if you used the same pathes as were used in this tutorial, just paste this: `C:\Program Files\Python311\python.exe -m venv .venv3`) <br>
12. Then activate it: `.\.venv3\Scripts\activate`. <br>
13. Now you need to setup a Python 2 virtual environment. Open the second terminal:<br>
<img alt="07_create_terminal" src="https://github.com/user-attachments/assets/c2ab2df1-f5d0-43cf-839d-5a1f94f361d3" />  <br>
14. Go to `.\My-naoqi-project\server` folder using this command `cd ..\client`. <br>
15. Create a new virtual environment from Python 2: `<your-path-to-python2-folder>\python.exe -m virtualenv .venv2` (if you used the same pathes as were used in this tutorial, just paste this: `C:\Program Files\Python27\python.exe -m virtualenv .venv2`) <br>
16. Then activate it: `.\.venv2\Scripts\activate`. <br>
17. So you will be having two terminals: one opened at `.\My-naoqi-project\server` folder with activated virtual env. for Python 2 and second opened at `.\My-naoqi-project\client` folder with activated virtual env. for Python 3.
18. To try to run a Python 3 program on NAOqi3, navigate to `.\My-naoqi-project\client\config.py` and uncommit or create NAO IP address and NAO port.
19. Then run `naoqi_server.py` in Python 2 terminal running this command: `python naoqi_server.py`. If everything is OK, you will se this output in your terminal: <br>
<img alt="08_run_server" src="https://github.com/user-attachments/assets/e70fd63b-eb9b-4fc0-be97-c7cfaf41b4f2" />  <br>
20. After this you can try to run any Python 3 test example from folder `client\examples`. Try to run in Python 3 terminal for example: `python .\examples\core\test_say_hello.py`.

**You have successfully installed NAOqi3 and setup your project!**


**❗️❗️❗️ Important information ❗️❗️❗️**

After successfully installing and launching NAOqi3, you can remove all `examples\` folders (both in `server\` and `client\`) or leave it for inspiration. Also delete the `pynaoqi.rar`, because we don't need it anymore. All files you actually require are: `client\naoqi_client.py`, `client\fetch_naoqi_constants.py`, `client\config.py` (to have NAO configs stored), `client\naoqi3.py`, `server\naoqi_server.py`, `server\proxy_service.py`.

## How to use it?

You will be working with `naoqi3.py` file from `client\` folder. This module is an absolute simulator of NAOqi SDk. It means that you should behaive with it in the same way as with original NAOqi library. <br>

**For example**: if you write a code to make a NAO robot say `"Hello World!"`, in original NAOqi library it will look like this:
```Python
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.setLanguage("English")
tts.say("Hello World!")
```
In NAOqi3 it will look almost the same:
```Python
from naoqi3 import ALProxy
tts = ALProxy("ALTextToSpeech", IP, PORT)
tts.setLanguage("English")
tts.say("Hello World!")
```

To create other programs for NAO you can look at [`examples\`](client/examples) folder or study the [official NAOqi SDK documentation](http://doc.aldebaran.com/2-1/dev/python/index.html).

### Working the NAOqi3

1. To start the NAOqi3 application, you firstlly need to run the server `naoqi_server.py`. Just open a terminal in `server\` folder and run: `python naoqi_server.py`.
2. After the server was started, you can run any of your code in normal way. <br>
❗️ **Notice**: Place all your python files that you want to run with NAOqi3 inside `client\` folder!
3. For example create a file `test.py`, add some Python 3 code inside it (for instance the code from the example above, but change `IP` and `PORT` to your values) and save this file to `client\` folder. Then open a terminal in the same folder and run: `python test.py`. <br>

**In such simple way you can run any Python 3 program you want!**

### Generate constants

NAOqi3 also implements an opportunity to dynamically generate all files with specific NAOqi original constants for this particular NAOqi SDK that you are using. Basically, it means that original NAOqi SDK contains some Python files (for example `motion.py`), that store specific constants that are used in vision configurations, motion configurations and so on. These files with constants can differ from NAOqi version 2.1.4 to version 2.8.6 for example. So all you need is just to generate these files once manually and you will be able to use it in your future programs! <br>

**The proces is very simple**:
1. Open a terminal in `client\` folder.
2. Then run: `python fetch_naoqi_constants.py`
3. And there will be two constants file generated (for NAOqi 2.1.4): `motion.py` and `vision_definitions.py`.

**You have successfully generated files with constants from original NAOqi SDK!**

## Functionality description

### Project Structure
```shell
project_root/
├── server/                         # Server-side code (Python 2)
│   ├── examples/                   # Directory with test programs
│   ├── config.py                   # Congifuration file: IP, PORT for Nao
│   ├── naoqi_server.py             # Server to execute NAOqi commands
│   ├── proxy_service.py            # File to cache proxies
│   ├── fetch_naoqi_constants.py    # Runable file to import all NAOqi constants
│
├── client/                         # Client-side code (Python 3)
│   ├── examples/                   # Directory with test programs
│   ├── naoqi3.py                   # Wrapper to emulate NAOqi in Python 3
│   ├── naoqi_client.py             # Client to communicate with Python 2 server
│   ├── config.py                   # Congifuration file: IP, PORT for Nao
│
└── README.md                       # Project documentation
```

### Server part
The server part of the system represents the communication element between the client and the original library NAOqi. The main task of the server is to receive requests from NAOqi3, perform the appropriate operations on NAOqi SDK objects and returning the results of these operations back to to the client side. Due to the need for direct communication and cooperation with the library NAOqi, the entire server subsystem is built in Python 2. Server part consists of two components: the file `naoqi_server.py` and the file `proxy_servis.py`.

### Client part
The client part of the system serves as an interface between the Python 3 environment and the original library NAOqi, which runs in Python 2. Its main task is to send requests to the server and simulate the interface known from the NAOqi API. The entire client side is implemented is implemented in Python 3 and consists of three modules: `naoqi3.py`, `naoqi_client.py` and `fetch_naoqi_constants.py`.

## FAQ
**_I have already installed another version of Python, will NAOqi3 work with it?_** <br>
Yes, the NAOqi3 will work on any Python 3 version, but if you want to use existing examples from this repository (for example `final-program\`), consider using the same Python version (3.11.0) that was used for developing this program. <br>
<br>
<br>
**_Where can I find information about my PC system architecture?_** <br>
You can find your PC system architecture in "Settings"->"System" find a frame "Device Specifications" and find a raw "System type". <br>
<br>
<br>
**_While running `python --version` I get error "python is not recognised as an internal or external command..."_** <br>
It means that your Python wasn't added to PATH variable during the installation process or the Python wasn't installed correctly. Try to find a solution with this [link](https://stackoverflow.com/questions/17953124/python-is-not-recognized-as-an-internal-or-external-command). Or try to reinstall Python following step-by-step the provided tutorial. <br>
<br>
<br>
**_I don't have a git system installed, what should I do?_** <br>
If you don't have a git system installed on your PC, follow this [official webpage tutorial](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), find a section "Install git on Windows" and follow all its steps. <br>
<br>
<br>
**_I get an error while trying to clone the remote repository. How to fix it?_** <br>
If you are getting an error while cloning the remote repository, firstly, check if your internet connection is working. If yes, visit the [GitHub Troubleshooting page](https://docs.github.com/en/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors). <br>
<br>
<br>
**_I get an error while running `naoqi_server.py`, how to fix it?_** <br>
Check if you have activated your `.venv2` virtual environment. In the opened terminal you should see `(.venv2)` in the beginning of the command line.<br>
<br>
<br>
**_I get an error while running Python 3 programs on NAOqi, how to fix it?_** <br>
1. If you have an error `Exception: ALBroker::createBroker, Cannot connect to tcp://...`, check the `client\config.py` if you have correct IP and PORT for your NAO robot. Also check the LAN connection to the robot.
2. If you have an import Error `ImportError: No module named naoqi`, visit the [Aldebaran Troubleshooting webpage](http://doc.aldebaran.com/2-5/dev/python/tips-and-tricks.html) and find the solution based on your case.
<br>
<br>






