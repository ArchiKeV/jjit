# JJIT is an alternative frontend for justjoin_it

The backend is written on the basis of the `fastapi` web framework using the `Jinja2` templating engine and the ASGI web server `uvicorn`

The frontend is written in pure `JavaScript` and pure `CSS`

The interaction with the database takes place using the `SQLAlchemy` ORM framework

![](https://raw.githubusercontent.com/ArchiKeV/jjit/main/jjit.png)

## How to run:

### Unix:

To download and run this project, you need to install `git`

1. Launch terminal in the folder for this project  
2. Clone project repository - `git clone https://github.com/ArchiKeV/jjit.git`
3. Go to project folder - `cd jjit`
4. Allow execution of `init.sh` and `run.sh` files - `chmod + x init.sh run.sh`
5. Run `init.sh` for the first time - `./init.sh`  
6. Run `run.sh` in a terminal every time you need to run a project - `./run.sh`

### Windows:

To download and run this project, you need to install `git`, `python` and `vc_redist.x64`

[Git](https://git-scm.com/download/win), [Python](https://www.python.org/downloads/windows/), [VC Redist](https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)

1. Launch terminal in the folder for this project  
2. Clone project repository - `git clone https://github.com/ArchiKeV/jjit.git`
3. Go to project folder - `cd jjit`
4. Run `init.bat` for the first time - `init.bat`
5. Run `run.bat` in a terminal every time you need to run a project - `run.bat`

## Features:

1. All filters except "Skills" and "Companies" are selected with "OR" logic

2. In the "Skills" and "Companies" filters, you can include or exclude the desired option - the included options will be circled in green, and the excluded ones - in red.

3. In the "Companies" filter, you can select the prepared preset "Add visa PBH companies". This preset includes in the filter the companies listed on the gov.pl website in the Poland.Business Harbor visa section
