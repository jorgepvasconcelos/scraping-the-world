# scraping-the-world

## Built With:

- [Python](https://www.python.org/) - Programming language
- [Flask](https://flask.palletsprojects.com/en/2.0.x/#) - Web Framework
- [Selenium](https://www.selenium.dev/) - Scraping Tool
- [Request-Html](https://docs.python-requests.org/projects/requests-html/en/latest/) - Scraping Tool
- [Pytest](https://docs.pytest.org/en/7.1.x/) - Test Framework
- [MySQL](https://www.mysql.com/) - DBMS


### System Requirements
- python ^3.9
- docker

### How to run
    make run

### How to run dev
    1 - Change "ENV" param value to "DEV"  in .env file
    2 - python scraping_the_world/app.py

### How to run tests
    make run
    make test

### How to run dev tests
    1 - Change "ENV" param value to "DEV"  in .env file
    2 - python scraping_the_world/app.py
    3 - make test

### Api documentation
Open with postman the file "scraping-the-world.postman_collection.json"

### Project structure
    - scraping-the-world
        - /scraping_the_world # Code source
            - /exception # Erros That will be raised from code
            - /models # Interection with Database
            - /routes # Api routes from aplication
            - /scrapers # Sites Scrapers
            - app.py # File that starts the code
        -/test # All test from aplication
        -/envs # Environment that can be used in aplication
    