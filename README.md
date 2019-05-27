## Installation

#### Postgres Setup

1. Install Postgres

    	brew install postgres@9.6

2. Create database

    ```
    createdb purchase_log
    ```

#### Setup `pipenv`

1. Install `pyenv`

    	brew install pyenv

[More Installation info](https://github.com/pyenv/pyenv#installation)


2. Install `pipenv`

    	pip install pipenv

3. Install dependencies

    	pipenv install

4. From here, you can access the pipenv shell

    	pipenv shell


#### Run application

1. Run migrations while in `pyenv` shell

    	flask db upgrade

2. Add secret key to `application.cfg`

3. Run application

    	python app.py


## Further Updates

1. Add authentication using 3rd party service such as Okta, Auth0, etc.
    * Would require table `Users` to keep track of username login information, password information would not be stored
    * Depending on authentication method (JWT, OAuth) could require table to keep track of session information
2. Add additional functionality to update customer address
    * Query DB using `customer.id` to see if Customer exists in db and update address field
3. Separate Models from views
    * Add a separate `models.py` file
    * Add a separate `views.py` file
4. Add testing using `pytest`
    * Use `pytest` to set up unit and itegration tests for views and utils
    * Add factorings using `factory_boy` to mock db data
5. Increase support for large files
    * Do load testing with larger files
    * Look into using pandas or other python libraries to process in chunks and if necessary in parallel
    * Add progress bar incorporating css style library such as bootstrap
6. Add docker container to setup environment and postgres to reduce installation instructions
7. Add indexes to primary keys fields to improve performance