# WildBoost API
## Сменить язык: [Русский](README.md)
***
API for the [bidder program](https://github.com/dyanashek/Wildboost-app), which automatically manages bids on the Wildberries advertising auction. The program determines the real rates (for advertising in search / advertising in the product card). And it keeps the user-specified position or range of positions without exceeding the specified budget.

## API functions:
1. Implementation of registration, authorization and related processes (change, password recovery, etc.)
2. Checking the payment status
3. Track subscription level and expiration date
4. Administrator interface using standard Django tools

## Installation and use:
- Create an .env file containing the following variables:
> the file is created in the root folder of the project
   - **SECRET_KEY** - Django secret key
   - **DEBUG** - testing mode (enabled with value = 1)
   - **ALLOWED_HOSTS** - allowed hosts
   - **ACCOUNT_ID** - YUkass (*russian payment service*) account ID
   - **SECRET_KEY_PAYMENT** - secret key of YUkass (*russian payment service*)
- Install the virtual environment and activate it (if necessary):
> Installation and activation in the root folder of the project
```sh
python3 -m venv venv
source venv/bin/activate # for macOS
source venv/Scripts/activate # for Windows
```
- Install dependencies:
```sh
pip install -r requirements.txt
```
- Migrations:
> Proceed to the folder containing manage.py (wb_bidder)
```sh
python3 manage.py makemigrations
python3 manage.py migrate
```
- Run project:
```sh
python3 manage.py runserver
```