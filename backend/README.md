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
├── mock_rsa_keys.py *** mocks authorization from Auth0 account
├── populate.py *** initially seed our database and test database.
├── requirements.txt *** dependencies to install with "pip3 install -r requirements.txt"
└── setup.sh
```

## API Reference

### Getting Started

- Backend URL: https://birds-of-the-world-backend.onrender.com
- Frontend URL: https://birds-of-the-world-frontend.onrender.com

### Authentication: How go get a token

#### Option 1

Get the values for the variables below from the project submission notes.

```
AUTH0_DOMAIN
ALGORITHMS
API_AUDIENCE
AUTH0_CLIENT_ID
```

Replace the variables in the URL below

```
https://{{AUTH0_DOMAIN}}/authorize?audience={{API_AUDIENCE}}&response_type=token&client_id={{AUTH0_CLIENT_ID}}&redirect_uri=http://localhost:3000
```

Paste the URL in a browser and use the username and password provided in the project submission notes.
This will result in a token being returned in the browser URL. This token can be copied and used for cURL requests.

#### Option 2

- run the setup.sh file provided in the submission notes: `source setup.sh`.
- run `python get_auth0_token.py`
- copy the tokens printed by the `python get_auth0_token.py` script in cURL requests

### Example cURL requests

#### List all birds

`curl -X GET -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/birds'`

#### Add a new bird

`curl -X POST -H 'Authorization: bearer eyToken' -H "Content-type: application/json" -d '{"common_name": "Test flamingo","habitats": [2, 3],"image_link":"example url","species": "Phoenicopterus ruber"}' 'https://birds-of-the-world-backend.onrender.com/birds'`

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
- Permission: get:birds
- Request Arguments: `page` - integer, `limit` - integer
- Returns: An object with 10 paginated birds, total birds and success state

example curl:

`curl -X GET -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/birds'`

example response:

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
- Permission: get:birds
- Request Arguments: `bird_id` - integer
- Returns: An object containing a bird object and success state

example curl:

`curl -X GET -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/birds/1'`

example response:

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
- Permission: post:birds

example curl:

`curl -X POST -H 'Authorization: bearer eyToken' -H "Content-type: application/json" -d '{"common_name": "Test flamingo","habitats": [2, 3],"image_link":"example url","species": "Phoenicopterus ruber"}' 'https://birds-of-the-world-backend.onrender.com/birds'`

example request body:

```json
{
  "common_name": "Test flamingo",
  "habitats": [2, 3],
  "image_link": "example url",
  "species": "Phoenicopterus ruber"
}
```

example request response:

```json
{
  "bird": 1,
  "success": true
}
```

---

`PATCH '/birds/{bird_id}'`

- Sends a patch request in order to edit a specified bird
- Permission: patch:birds
- Request Arguments: `bird_id` - integer

example curl:

`curl -X PATCH -H 'Authorization: bearer eyToken' -H "Content-type: application/json" -d '{"common_name": "bird patched","habitats": [2, 3],"image_link":"example url","species": "Phoenicopterus ruber"}' 'https://birds-of-the-world-backend.onrender.com/birds/1'`

example request body:

```json
{
  "common_name": "Test flamingo patch",
  "habitats": [2, 3],
  "image_link": "example url",
  "species": "Phoenicopterus ruber"
}
```

example request response:

```json
{
  "bird": 1,
  "success": true
}
```

---

`DELETE '/birds/{bird_id}'`

- Deletes the bird that has the ID that was in the query parameter if it exists.
- Permission: delete:birds
- Request Arguments: `bird_id` - integer
- Returns: the id of the deleted bird, success value

example curl:

`curl -X DELETE -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/birds/1'`

example request response:

```json
{
  "deleted": 1,
  "success": true
}
```

---

`GET '/habitats?page=${integer}&limit=${integer}'`

- Fetches a list of habitat objects, success state and total habitats
- Permission: get:habitats
- Request Arguments: `page` - integer, `limit` - integer
- Returns: An object with 10 paginated habitats, total habitats and success state

example curl:

`curl -X GET -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/habitats'`

example response:

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
- Permission: get:habitats
- Request Arguments: `habitat_id` - integer
- Returns: An object containing a habitat object and success state

example curl:

`curl -X GET -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/habitats/1'`

example response:

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

- Sends a post request in order to add a new habitat
- Permission: post:habitats

example curl:

`curl -X POST -H 'Authorization: bearer eyToken' -H "Content-type: application/json" -d '{"name": "Test Europe","region_id": 1}' 'https://birds-of-the-world-backend.onrender.com/habitats'`

example request body:

```json
{
  "name": "Europe",
  "region_id": 1
}
```

example request response:

```json
{
  "habitat": 3,
  "success": true
}
```

#### Search Habitats

- Fetches a list of habitat objects that has a name key that value contains the search term that was supplied in the request argument.
- Permission: post:habitats
- Search term is case insensitive
- Returns a list of habitat objects filtered by the specified search. And a success value, total number of habitats,

example curl:

`curl -X POST -H 'Authorization: bearer eyToken' -H "Content-type: application/json" -d '{"search": "Af"}' 'https://birds-of-the-world-backend.onrender.com/habitats'`

example request body:

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
- Permission: patch:habitats
- Request Arguments: `habitat_id` - integer

example curl:

`curl -X PATCH -H 'Authorization: bearer eyToken' -H "Content-type: application/json" -d '{"name": "Patched habitat","region_id": 1}' 'https://birds-of-the-world-backend.onrender.com/habitats/1'`

example request body:

```json
{
  "name": "West Europe",
  "region_id": 2
}
```

example request response:

```json
{
  "habitat": 1,
  "success": true
}
```

---

`DELETE '/habitats/{habitat_id}'`

- Deletes the habitat that has the ID that was in the query parameter if it exists.
- Permission: delete:habitats
- Request Arguments: `habitat_id` - integer
- Returns: the id of the deleted habitat, success value

example curl:

`curl -X DELETE -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/habitats/1'`

example request response:

```json
{
  "deleted": 1,
  "success": true
}
```

---

`GET '/regions'`

- Fetches a list of regions objects and success state
- Permission: get:regions
- Request Arguments: None
- Returns: An object with regions and success state

example curl:

`curl -X GET -H 'Authorization: bearer eyToken' -H "Content-type: application/json" 'https://birds-of-the-world-backend.onrender.com/regions'`

example response:

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
export AUTH0_CLIENT_ID=
export AUTH0_CLIENT_SECRET=
export AUTH0_OWNER_USERNAME=
export AUTH0_OWNER_PASSWORD=
export AUTH0_VIEWER_USERNAME=
export AUTH0_VIEWER_PASSWORD=
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

_Note:_ The tests mocks authentication and permission roles. It is possible to run `python3 -m unittest local/test_auth0_token.py` for tests with real auth0 tokens. It is important to define all the environments secrets. 
