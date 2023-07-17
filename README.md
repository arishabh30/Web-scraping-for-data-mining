# WebScraping for data mining
Add the weekly progress to the following [ppt](https://docs.google.com/presentation/d/1fFANXCziJra5UxJyQGE0Wz0FS7KVJR_XYhk-lk86lYM/edit#slide=id.p).

## To run the Flask application on your system:
1. Clone the repository on your computer
2. Ensure that Python is installed on your computer
     - For Windows:
         In cmd, type `python3 -version`
     - For Ubuntu:
         In the terminal, type `python3 -v`
3. Install pip in your **Ubuntu** system if not present using `sudo apt-get install python3-pip`
3. Move into the project directory, here directory is named **flask_app**
4. Install venv using
     - For Windows:
             type `pip install venv`
     - For Ubuntu:
             type `pip install venv`
5. Create a Python virtual environment in the current directory
   - For Windows:
                       type `python3 -m venv venv`
   - For Ubuntu:
                        type ` python3 -m venv venv`
6.  Activate the virtual environment using the following command
   - For Windows:
             type `.\venv\Scripts\activate`
    - For Ubuntu:
             type `source venv/bin/activate`
7.  Now you are in the virtual environment named `venv`
8.  Run the following command to install **flask** in your virtual environment
     - `pip install Flask`
9.  To install the necessary dependencies
      -  Run this command to install _pipreqs_ library `pip install pipreqs`
      -  After successful installation, run the command `pipreqs`
          - This will create a `requirements.txt` file
      - Now run this command to install all the libraries required to run the program `pip install -r requirements.txt`
10. Now to execute the code:
      - For Windows : `set FLASK_APP=hello.py` followed by `flask run`
      - For Ubuntu : `export FLASK_APP=hello.py` followed by `flask run`
       
