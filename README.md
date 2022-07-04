# Python-etl2

Python-etl2 is a program developed in Python, with the purpose of downloading files from the web https://prestadores.minsalud.gov.co and inserting their records in a SQL Server database

## Features

- Allows downloading of all preconfigured files continuously and automatically.
- Allows downloading files individually passed as argument the name of the required file.

## Tech

Dillinger uses a number of open source projects to work properly:

- [Python](https://www.python.org/) - Programming language
- [Selenium](https://www.selenium.dev/) - Automation library
- [Webdrive-manager](https://pypi.org/project/webdriver-manager/) - manager for automatic driver download and update.

To see a complete list of the libraries used, you can see the following document [here](https://github.com/dataf3l/python-etl2/blob/main/src/requierement/prod/requierements.txt)

## Installation

Python-etl2 requires [Python](https://www.python.org/) v3.5+ to run.

### Set the environment variables

Set the environment variables according to the execution environment (prod/dev) in the following files:

* config/env/prod/.env
* config/env/dev/.env

 **Variable list:**

| Argument    | File name                                       | Example               |
| ----------- | ----------------------------------------------- | --------------------- |
| SERVER_NAME | The database server name                        | 'server_name'         |
| DATABASE    | The data base name                              | 'database_name'       |
| USER_NAME   | username with permission to access the database | 'user_name'           |
| PASSWORD    | User password                                   | 'supersecretpassword' |

#### Windows

Installation instructions on windows operating system:

Create and activate virtual environment

```sh
cd python-etl2
py -m venv VENV
VENV\Scripts\activate.bat
```

Install dependencies

```sh
cd srcapp\requierement\prod
py -m pip install -r requierements.txt
```

Run the program in development mode; will run the program and download all the predefined files.

```sh
py src\app\automate.py
```

Run the program in development mode with parameters; will run the program and download the specified file.

```sh
py src\app\automate.py -f prestadores
```

#### Linux

Installation instructions on linux operating system:

Install ODBC driver

```sh
sudo apt-get install unixodbc-dev
```

Create and activate virtual environment

```sh
cd python-etl2
python3 -m venv VENV
source VENV/bin/activate
```

Install dependencies

```sh
cd srcapp/requierement/dev
python3 -m pip install -r requierements.txt
```

Run the program in development mode; will run the program and download all the predefined files.

```sh
python3 src/app/automate.py
```

Run the program in development mode with parameters; will run the program and download the specified file.

```sh
python3 src/app/automate.py -f prestadores
```

#### Arguments list

 **Flat:**  -f
Default value: all

| Argument    | File name                  |
| ----------- | -------------------------- |
| prestadores | Prestadores.csv            |
| sedes       | Sedes.csv                  |
| servicios   | Servicios.csv              |
| capacidad   | CapacidadInstalada.csv     |
| seguridad   | MedidasSeguridad.csv       |
| sanciones   | MedidasSeguridad (1).csv * |
| all         | all files                  |

**Flat:**  --mode
Default value: prod

| Argument | Description            |
| -------- | ---------------------- |
| prod     | run in production mode |
| dev      | run in developer mode  |


Examples (Linux):

```sh
./run.sh --mode dev -f sanciones
```

Examples (Windows):

```sh
.\run.bat --mode dev -f sanciones
```

#### Building for source

For production release:

```sh
pyinstaller src/app/automate.py
```

## Docker

In order to be able to develop and test software around Linux development, an docker-compose.yml file has been created to build a Docker container with a SQL Server image.

```sh
docker-compose -f config/docker/docker-compose.yml up  --remove-orphans -d
```

**Note:** Requiere install docker-compose and Docke
