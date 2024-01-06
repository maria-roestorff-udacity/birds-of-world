# Backend - Birds of the World App

This section contains the code for the backend of the Birds of the World App. The backend uses **Flask** as the server framework and is written in **Python**.

## Backend Tech Stack

- **venv** Create and activate a virtual python environment
- **PostgreSQL** Database
- **SQLAlchemy** SQL toolkit and ORM to map Python objects to SQL tables
- **Flask-Migrate** Create and run schema migrations
- **Flask-CORS** Handle cross-origin requests from the frontend
- **Jose** JavaScript Object Signing and Encryption for JWTs

## Main Files: Project Structure

```sh
├── README.md
├── app.py *** the main controller and driver of the server.
                    "python app.py" to run after installing dependencies
├── models.py *** contains the SQLAlchemy models.
├── auth.py *** integration with Auth0 for authentication.
├── test_rbac.py *** unittests to test the server.
├── test_no_auth.py *** unittests without authentication.
├── populate.py *** initially seed our database and test database.
├── requirements.txt *** dependencies to install with "pip3 install -r requirements.txt"
├── runtime.txt
├── setup.sh
└── Procfile
```

## API Reference

### Getting Started

- Backend URL: TODO
- Frontend URL:
- Authentication: TODO

### Roles: `Owners` and `Viewers`

#### Viewers Permissions

- get:birds
- get:habitats
- get:regions

#### Owners Permissions

- get:birds
- get:habitats
- get:regions
- post:birds
- post:habitats
- patch:birds
- patch:habitats
- delete:birds
- delete:habitats

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: bad request
- 401: authorization header is expected
- 404: resource not found
- 405: method not allowed
- 422: unprocessable

### Endpoints and behaviors

`GET '/birds?page=${integer}&limit=${integer}'`

- Fetches a list of bird objects, success state and total birds
- Request Arguments: `page` - integer, `limit` - integer
- Returns: An object with 10 paginated birds, total birds and success state

```json
{
  "birds": [
    {
      "common_name": "American flamingo",
      "habitats": [
        {
          "id": 1,
          "name": "Galápagos Islands of Ecuador"
        }
      ],
      "id": 1,
      "image_link": "url",
      "regions": [
        {
          "image": "url",
          "name": "South America"
        }
      ],
      "species": "Phoenicopterus ruber"
    }
  ],
  "success": true,
  "total_birds": 1
}
```

---

`GET '/birds/{bird_id}'`

- Fetches a specified bird object and success state
- Request Arguments: `bird_id` - integer
- Returns: An object containing a bird object and success state

```json
{
  "bird": {
    "common_name": "American flamingo",
    "habitats": [
      {
        "id": 2,
        "name": "Galápagos Islands of Ecuador"
      },
      {
        "id": 3,
        "name": "Coastal Colombia"
      }
    ],
    "id": 1,
    "image_link": "url",
    "species": "Phoenicopterus ruber"
  },
  "success": true
}
```

---

`POST '/birds'`

- Sends a post request in order to add a new bird
- Request Body:

```json
{
  "common_name": "American flamingo",
  "habitats": [2, 3],
  "image_link": "url",
  "species": "Phoenicopterus ruber"
}
```

- Returns:

```json
{
  "bird": 3,
  "success": true
}
```

---

`PATCH '/birds/{bird_id}'`

- sends a patch request in order to edit a specified bird
- Request Arguments: `bird_id` - integer
- Request Body:

```json
{
  "common_name": "American flamingo",
  "habitats": [2, 3],
  "image_link": "url",
  "species": "Phoenicopterus ruber"
}
```

- Returns:

```json
{
  "bird": 3,
  "success": true
}
```

---

`DELETE '/birds/{bird_id}'`

- Deletes the bird that has the ID that was in the query parameter if it exists.
- Request Arguments: `bird_id` - integer
- Returns: the id of the deleted bird, success value

```json
{
  "deleted": 3,
  "success": true
}
```

---

`GET '/habitats?page=${integer}&limit=${integer}'`

- Fetches a list of habitat objects, success state and total habitats
- Request Arguments: `page` - integer, `limit` - integer
- Returns: An object with 10 paginated habitats, total habitats and success state

```json
{
  "habitats": [
    {
      "id": 1,
      "name": "Austalia",
      "region_id": 6
    },
    {
      "id": 2,
      "name": "Galápagos Islands of Ecuador",
      "region_id": 7
    }
  ],
  "success": true,
  "total_habitats": 2
}
```

---

`GET '/habitats/{habitat_id}'`

- Fetches a specified habitat object and success state
- Request Arguments: `habitat_id` - integer
- Returns: An object containing a habitat object and success state

```json
{
  "habitat": {
    "id": 1,
    "name": "Austalia",
    "region_id": 6
  },
  "success": true
}
```

---

`POST '/habitats'`

#### Post New Habitat

- sends a post request in order to add a new habitat
- Request Body:

```json
{
  "name": "Europe",
  "region_id": 1
}
```

- Returns:

```json
{
  "habitat": 3,
  "success": true
}
```

#### Search Habitats

- Fetches a list of habitat objects that has a name key that value contains the search term that was supplied in the request argument.
- Search term is case insensitive
- Returns a list of habitat objects filtered by the specified search. And a success value, total number of habitats,

```json
{
  "search": "a"
}
```

- Returns:

```json
{
  "habitats": [
    {
      "id": 1,
      "name": "Austalia",
      "region_id": 6
    },
    {
      "id": 2,
      "name": "Galápagos Islands of Ecuador",
      "region_id": 7
    }
  ],
  "success": true,
  "total_habitats": 2
}
```

---

`PATCH '/habitats/{habitat_id}'`

- Sends a patch request in order to edit a specified habitat
- Request Arguments: `habitat_id` - integer
- Request Body:

```json
{
  "name": "West Europe",
  "region_id": 2
}
```

- Returns:

```json
{
  "habitat": 3,
  "success": true
}
```

---

`DELETE '/habitats/{habitat_id}'`

- Deletes the habitat that has the ID that was in the query parameter if it exists.
- Request Arguments: `habitat_id` - integer
- Returns: the id of the deleted habitat, success value

```json
{
  "deleted": 3,
  "success": true
}
```

---

`GET '/regions'`

- Fetches a list of regions objects and success state
- Request Arguments: None
- Returns: An object with regions and success state

```json
{
  "regions": [
    {
      "id": 1,
      "image_link": "url",
      "name": "Africa"
    },
    {
      "id": 2,
      "image_link": "url",
      "name": "Antartica"
    },
    {
      "id": 3,
      "image_link": "url",
      "name": "Asia"
    },
    {
      "id": 4,
      "image_link": "url",
      "name": "Europe"
    },
    {
      "id": 5,
      "image_link": "url",
      "name": "North America"
    },
    {
      "id": 6,
      "image_link": "url",
      "name": "Oceania"
    },
    {
      "id": 7,
      "image_link": "url",
      "name": "South America"
    }
  ],
  "success": true,
  "total_regions": 7
}
```

---

## Development Setup

- [Python Installation](https://codesolid.com/installing-pyenv-on-a-mac/?utm_content=cmp-true)
- [Postgres Installation](https://daily-dev-tips.com/posts/installing-postgresql-on-a-mac-with-homebrew/?utm_content=cmp-true)

### Virtaul Python Environment

[Setup](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

```bash
python3 -m venv .venv
source .venv/bin/activate
which python3 # Check filepath is current and correct
```

### Environment Secrets

Secrets in the setup.sh

```bash
chmod +x setup.sh
```

If you want to run this repo locally with your own OAuth credentials you need to export the following environment variables

```
export DATABASE_URL=
export TEST_DATABASE_URL=
export AUTH0_DOMAIN=
export ALGORITHMS=
export API_AUDIENCE=
```

### Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Initial Database Creation

```bash
dropdb botwdb
createdb botwdb
```

### Run the Server

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
export FLASK_ENV=development
```

To run the server, execute:

```bash
flask run --reload
```

### Tests

In order to run tests navigate to the backend directory and run the following commands:

```bash
dropdb testbotwdb
createdb testbotwdb
python3 test_rbac.py
```

_Note:_ The tests works with Authentication and permission roles. Thats why all the secret environments should be defined. It is possible to run `test_no_auth.py` for tests without authentication.
