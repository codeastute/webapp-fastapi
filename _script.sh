# # # Python and venv

# Installing python, pip and venv
sudo apt -y install python3.11
sudo apt -y install python3-pip
sudo apt -y install python3.11-venv

# Creating the venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
which python
which pip

# Installing libraries
vi requirements.txt
fastapi[standard]>=0.112.0,<0.113
SQLAlchemy>=2.0.32,<2.1
passlib>=1.7.4,<1.8
bcrypt>=4.2.0,<4.3
python-jose>=3.3.0,<3.4
python-dotenv>=1.0.1,<1.1
pydantic>=2.8.2,<2.9

pip install -r requirements.txt
pip list




# # # Github
https://github.com/adeloaleman and create a repository: fastapi
https://github.com/github/gitignore
vi .gitignore
touch README.md
git init
git branch -M main
git branch --show-current
git add . 
git add -A
git commit -m 'first commit'
git remote add origin git@github.com:adeloaleman/fastapi.git
git remote add origin git@github-codeastute:codeastute/fastapi.git
git remote set-url origin git@github.com:adeloaleman/fastapi.git   # In case we want to modify it
git push -u origin main 




# # # Fastapi project
vi .env
AUTH_SECRET_KEY=197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3
AUTH_ALGORITHM=HS256
API_URL=http://localhost:3000

touch Procfile

mkdir api
touch api/__init__.py
touch api/main.py
touch api/database.py
touch api/deps.py
touch api/models.py
mkdir api/routers
touch api/routers/__init__.py
touch api/routers/auth.py




mkdir .vscode
touch .vscode/settings.json
{
    "explorer.sortOrder": "filesFirst"
}