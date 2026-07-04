# Pet Web - Full Stack SPA 

# 🐶 Pet Web - Our Dogginho Care System 🐾 🐕 🐕 🦺 🦺

Welcome to the Pet Web! This system allows you to register your information and those of your puppy, receiving personalized tips and care based on the breed, you can view the respective photos of the breed. The information after registration or login will be sampled in the cards below the form. In addition to registration and visualization, it is also possible to modify or delete the information. 

**Welcome to Pet Web! **

This system allows users to register their own information as their dog’s information, receiving personalized tips and care recommendations based on the dog’s breed. Users can also view photos related to each breed.

After registration or login, the submitted information is displayed in cards below the form. In addition to registering and viewing data, users can also update or delete their information.

**Willkommen bei Pet Web! **

Dieses System ermöglicht es Benutzerinnen und Benutzern, ihre eigenen Informationen sowie die Informationen ihres Hundes zu registrieren und personalisierte Tipps und Pflegehinweise basierend auf der Hunderasse zu erhalten. Außerdem können passende Photos der jeweiligen Rasse angezeigt werden.

Nach der Registrierung oder Anmeldung werden die eingegebenen Informationen in Karten unterhalb des Formulars angezeigt. Neben dem Registrieren und Anzeigen der Daten ist es auch möglich, die Informationen zu bearbeiten oder zu löschen. 

#⚙️ In the future, it may be chosen: 

> <span style="color: #9543f9;"> 🥣 Different types of Feeds,</span> <span style="color:magenta;"> 🧴 Care Products for your dog</span>, <span style="color:#70CC87;"> 🩺 Veterinarians in your region,</span>
>> > In the future it will be possible to monetize Content - convert traffic or online content into revenue, (affiliate marketing, direct advertising, sponsored content and other strategies).


## Modularized Structure 

The backend following the standard taught in the Dev discipline. Full Stack Basic - PUC:
- ✅ **`model/`** - Separate models (User, Raca, Dog)
- ✅ **`schemas/`** - Pydantic validation schemes
- ✅ **MVC Organization** - Modular and scalable code

## Pet Web - Modularized Structure

## 📁 Structure

The project previously, I had not modularized, I made the modifications, following the standard MVC (Model-View-Controller) taught in class, 
I separated the responsibilities of the project modules, organizing the code into separate modules:

````
backend/
├─ app.py ✅ Main - API routes and endpoints (Controller)
├── seed_db.py ✅ Populate the bank (NECESSARY!) - Script for popular the bank
├── requirements.txt ✅ Dependencies - Dependencies that must be installed (pip)
├─ swagger.yaml ✅ API documentation
├── README.md ✅ Instructions
├─ .gitignore ✅ Protection - files that must be ignored by git
├─ model/ ✅ Models
│ ├── __init__.py # package launcher -Initializes DB and exposes the templates- (Purpose: Sets a directory
│ │ as a Python package)
│ ├─ base.py # SQLAlchemy base
│ ├─ user.py # User Model
│├── raca.py # Model Raca
│ └── dog.py # Model Dog
└─ schemas/ ✅ Validation - Validation schemes (Pydantic)
│ ├── __init__.py # package launcher - Exposes all schemas
│ ├─ error.py # Error scheme
│ ├─ user.py # User Schemas
│ ├── raca.py # Raca Schemas
│ └─ dog.py # Dog Schemas
├── Venv/ # After installation - the virtual environment
└─ instance/ # After installation - SQLite database
    └─ site.db

````

# 🐶 Project

This is a basic, Full-Stack project developed as a Single Page Application (SPA) for the "Pet Web" as per the project's graphic wireframe. The goal is to demonstrate the integration of a Python backend (Flask) with an interactive frontend (HTML, CSS, JavaScript), using Pydantic for data validation and Flask-OpenAPI3 for API documentation (Swagger UI). Following the "requirements for MVP.pdf"

[Link: The graphical wireframe similar to page -first prototype-](https://github.com/user-attachments/assets/222aa8f9-9262-4d1f-ad27-a35acae0f414)


<img width="1382" height="769" alt="image" src="https://github.com/user-attachments/assets/222aa8f9-9262-4d1f-ad27-a35ae0f414" />


## Technologies Used
Backend in Python using Flask and Flask-SQLAlchemy. Provides endpoints to manage users, breeds and dogs.

## Backend:

    Python3
    Flask: Microframework web
    Flask-OpenAPI3: OpenAPI/Swagger UI Integration with Flask and Pydantic
    Pydantic: Data validation (models for requests/responses)
    SQLAlchemy (ORM)
    SQLite3: Lightweight relational database
    Flask-CORS (Cross-Origin Resource Sharing)
    
## Frontend:

    HTML5: Page structure
    CSS3: Responsive Stylization
    JavaScript (ES6+): SPA interactivity, DOM manipulation, Fetch API requests    
    for the backend

# Pet Web — Backend (API)

## Download or clone the pet-web-backend.zip file


**⚠️ IMPORTANT:** After cloning the two repositories (pet-web-backend and pet-web-frontend), rename the folders to "backend" and "frontend" respectively, as the backend serves both the API and the frontend in port 5000, and the code fetches the frontend folder a level above the backend (../frontend). The responsible line of code is in `app.py` line 384:
```python
frontend_dir = os.path.abspath(os.path.join(basedir, '...', 'frontend'))
````
 
### Prerequisites
Make sure you have the python, or python3 and pip (Python package manager) installed on your system. 
SQLite3 usually comes pre-installed and with python3 on macOS.

# Backend — Pet Project

## This directory contains the Flask API used by Project Pet.

### Requirements - follow the steps -
```diff
- Create a virtual (recommended) environment
- Python 3.8+ (on mac, to use/exclude Python, python3 [option] | file , e.g. python3 app.py)
- Install dependencies

. IMPORTANT:! Before starting the server (python3 app.py), run:
> rename the folders to "backend" and "frontend"
> python seed_db.py
> This command populates the bank with 24 breeds of dog necessary for the operation of the system.
> Follow the step by step below

````
## Step by Step
### In the Terminal - for example from vs-code

⇥ 1. Go to the director
````
 cd backend/ (rename the folders to "backend" and "frontend" after download or clone)
````

⇥ 2. Create the virtual environment of the project with name venv
````
 python3 -m venv venv
````
⇥ 3. To activate the virtual environment:
````
 source venv/bin/activate # Mac/Linux
````
````
 venv\Scripts\activate # Windows
````
**💡 Tip:** To confirm that it is in the correct environment, the terminal must show `(venv)` at the beginning of the line.

⇥ 4. Install dependencies:
````
 pip install -r requirements.txt
````

## Running locally

⇥ 5. initializes the bank (if necessary- if it does not yet exist)
````
 python3 seed_db.py
````
    > This command will:
      Create the instance/ folder (if it doesn't exist)
      Create the site.db bank
      Inserts 24 breeds of dog

⇥ 6. run app
````
 python3 app.py
````
````
# The API will be available at http://127.0.0.1:5000

````

## If it exists - Permission Error when Recording Data ⚠️ Troubleshooting - if directories do not allow writing

If you receive JSON (, , ,) errors or permission error when trying to register data, you need to adjust the direct write permissions of the `instance/` folder:

```bash
# Give writing permission in the instance folder
chmod -R 755 instance/

# If necessary, restart the server:
#1. Stop the server (Ctrl+C in the terminal)
#2. Disable and reactivate the virtual environment:
deactivate
source venv/bin/activate # Mac/Linux

#3. Clear Python cache (if necessary):
find . -type d -name __pycache__ -exec rm -rf {} +

#4. Restart the server:
python3 app.py
````

## Database
- The bank is a SQLite file in `/instance/site.db`
- [Image link](https://github.com/user-attachments/assets/8a186726-e2ee-459b-845a-6a458b49ec)
 
<img width="564" height="453" alt="image" src="https://github.com/user-attachments/assets/862b9cf7-c4e9-4509-8322-17be0c0e70ee" />
  <img width="1202" height="196" alt="image" src="https://github.com/user-attachments/assets/44d34dca-bbd4-4f41-af5d-3b4d3130f923" />


  ## To upload data for already related testing 
  > In the bank, the user tables, and dog, are for registration through the forms (via POST), comes at first empty, but with the following
  > commands can be uploaded test data that are available as .sql files in the repository:
  > ### To upload user data:
     > sqlite3 instance/site.db < user.sql
  > ### To upload dog data:
     > sqlite3 instance/site.db < dog.sql


# OpenAPI/Swagger documentation
- Access the UI Swagger at: `http://127.0.0.1:500/swagger`
- The `backend/swagger.yaml` file contains the complete specification of the routes.

**Main routes for demonstration (4 required by work)**
- `GET /racas` — list all breeds
- `GET /users/`— list all registered users. 
- `POST /users` — creates user (e.g. for registration)
- `POST /dogs` — breeds dog associated with `user_id` and `raca_id` (e.g. register pet)
