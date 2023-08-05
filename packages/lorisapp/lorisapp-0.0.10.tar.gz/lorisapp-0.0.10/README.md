# Loris
### Database and Analysis application for a Drosophila Lab (or any lab)

Loris is in development with core features still being tested and added.
Documentation for the different features will be added soon.

## Requirements

* Pip
* Git

## Pulling the source code

Pull the recent version of Loris:
```
git pull https://github.com/gucky92/loris.git
```

## Installation of API

Install using the pip command:
```
cd loris
pip install --user .
```

## Running App after API Installation

Create your own `config.json` file. There is a template file called `_config.json`.

If you do not have a running MySQL database yet, you can install a running SQL database by cloning a mysql-docker git repository and running docker-compose:
```
git clone https://github.com/gucky92/mysql-docker
cd mysql-docker/slim
sudo docker-compose up -d
```

To run the Loris app (in the main loris directory):
```
conda activate loris  # activate the environment if you haven't done so
python run.py
```
The app should now be running on port 1234.
