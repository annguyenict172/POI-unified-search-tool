# POI Unified Search Tool

### Description

Today, billions of quality POI data are accessible through various data providers, such as Foursquare, Google and Facebook. However, each provider has its own dataset and API, so users must work with each one in isolation, and manually identify duplicate data between providers.

This project aim to create an unified search tool where users can retrieve POI data from different providers using a single API only. The system can also automatically merge duplicate data between the providers.

### How to run

1. Install `python3.7`, `pip` and `virtualenv`.
2. Go to this folder `$ cd POI_unified_search_tool`.
3. Create a virtual environment `virtualenv venv --python=python3.7`.
4. Activate the virtual environment `source venv/bin/activate`.
5. Install the dependencies by running `pip install -r requirements.txt`.
5. Create a `.env` file and add the necessary API keys. Example can be seen in `.env.example`.
6. Create the SQLite database by running `$ flask db upgrade`.
7. Add the example list of categories by running `$ python script.py add_service_categories`.
8. Run the server by running `$ sh start.sh`. The server should be running in port 5000.

### Usage
After running the server, you can start making requests to `http://localhost:5000/places` to retrieve the POI data. Here are the list of parameters:
- `location`: the latitude and longitude of the location you want to search around. Example: `21.0278,105.8342`
- `radius`: the distance around the `location` parameter to search within. Example: `1000`
- `keyword`: the term to be searched against the place's name, address or category. Example: `pizza`
- `categories`: the list of categories which you are interested in. Example: `food,coffee`

The response will be given under this format:
```json
[
  {
    "facebook": {
      "description": "properties of this place in Facebook"
    },
    "foursquare": {
       "description": "properties of this place in Foursquare"
    },
    "google": {
       "description": "properties of this place in Google"
    }
  },
]
```