# KHADI-Timetable-Bot

## Requirements

* Python 3.9+

## Run

* Native
    1. Install all dependencies: `pip install -r requirements.txt`
    2. Set environment variables. The entire list can be found in the [example.env](example.env)
    3. Run main script `python main.py`

* Docker Compose
    1. Set environment variables in [example.env](example.env)
    2. Run command `docker-compose up`

* Docker
    1. Set environment variables in [example.env](example.env)
    2. Build image with command `docker build . -t bot`
    3. Run container `docker run --env-file example.env --name bot -it bot`