# NutritionInformation-Microservices

To run, you need to use **docker-compose up --build** command to create the containers.
Afterward you can issue HTTP commands using cURL/postman.

This application includes a Meals-Dishes service, a Diets service, a Database service, and a Reverse-proxy service. This setup is intended to ensure persistence, handle failures gracefully, and route requests appropriately using NGINX. Dishes values are retreived using calls to Ninjas API nutrition API with a key saved in .env within the dishes_meals directory.

The Database for both Meals and Diets services is persistent. Therefore, if the containers are stopped/paused/killed, when started again the Meals/Diets that were in the DB before shut down remain - as long as the volume isn't removed. In addition, if failure occurs the containers restart immediately.

There are 4 services that do the following:

1. **Meals-Dishes Service** - Manages meals and dishes information and provides endpoints to create and retrieve meals and dishe.
2. **Diets Service** - Manages diet information and provides endpoints to create and retrieve diets.
3. **Database Service** - Manages storage for meals and diets.
4. **Reverse-Proxy Service (NGINX)** - Routes external HTTP requests to the appropriate internal services.

The API endpoints:

* `POST /diets `
  Description: Adds a diet to the database.
  valid payload example (JSON):

  ```JSON
  {
  "name": "low sodium",
  "cal": 5000,
  "sodium": 5,
  "sugar": 50
  }
  ```
* `GET /diets  `
  Description: Retreives a list of all diet plans.
* `GET /diets/{name} `
  Description: Retreives a specific diet by its name.
* `POST /dishes  `
  Description: Adds a dish to the database, if successful returns the created dish's id.
  valid payload example (JSON):

  ```json
  { "name": "green salad" }
  ```
* `GET /dishes `
  Description: Retreives a list of all dishes.
* `GET /dishes/{id} `
  Description: Retreives a specific dish by its ID.
* `GET /dishes/{name} `
  Description: Retreives a specific dish by its name.
* `DELETE /dishes/{id} `
  Description: Deletes a dish with the given ID, if deletion was successful, returns that ID.
* `DELETE /dishes/{name} `
  Description: Deletes a dish with the given name, if deletion was successful, returns that dish's ID.
* `POST /meals `
  Description: Adds a meal to the database, if successful returns the created meals's id (used in meal creation).
  Note that the numbers given as inputs are valid dishes' ids that exist in the DB.
  valid payload example (JSON):

  ```json
  {
  "name": "Vegetarian Special",
  "appetizer": 1,
  "main": 5,
  "dessert": 9
  }
  ```
* `PUT /meals/{ID}   `
  Description: Updates the meal with the given ID (assuming it exists) with the given values.
  Payload's the same as when posting a new meal.
* `GET /meals?diet={name}`
  Description: Retreives a list of all meals whose all nutritional values are less or equal to the ones in the given diet.
* `GET /meals/{id} `
  Description: Retreives a specific meal by its ID.
* `GET /meals/{name} `
  Description: Retreives a specific meal by its name.
* `DELETE /meals/{id} `
  Description: Deletes a meal with the given ID, if deletion was successful, returns that ID.
* `DELETE /meals/{name} `
  Description: Deletes a meal with the given name, if deletion was successful, returns that meal's ID.

The ports used and their permissions:

1. 27017 - DB service port. Used by Meals and Diets services.
2. 5001 - Meals-Dishes service container port. Through this port GET/POST/PUT/DELETE operations are allowed on Meals resource and Dishes resource.
3. 5002 - Diets service container port. Through this port GET/POST/PUT/DELETE operations are allowed on Diets resource.
4. 80 - NGINX reverse proxy service container port. Through this port only GET requests to Meals-Dishes/Diets resources are allowed. Other operations are blocked and will return forbidden 403 code.
