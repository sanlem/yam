To install project:
1. create virtualenv:
virtualenv --python=/path/to/python3 /path/to/env/forled

2. activate virtual ennvironment:
source /path/to/env/folder/bin/activate

3. install requirements
cd to project root
pip install -r requirements.txt

4. prepare database
cd yam
./manage.py migrate

5. start dev server
./manage.py runserver

6. enjoy (or nor)
