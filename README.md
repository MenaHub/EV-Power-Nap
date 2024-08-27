# PowerNap - EV Charging Station Finder

PowerNap is an open-source web and mobile application designed to help users locate the optimal EV charging station based on factors such as proximity to the destination, duration of stay, charging speed, electricity costs, current battery level, and desired charge level.

This was a project we created in 24 hours as part of the [NOI Tech Park Summer 2024 Hackathon](https://hackathon.bz.it/project/powernap-1) in Scenna (BZ).
The app utilizes a heuristic algorithm to assign a score to each station, taking into account a weighted combination of these factors to ensure users receive the best possible recommendations.

Our public APIs provide easy access to a range of information, including walking distance from the charging station to the destination, station location, charging costs, provider details, socket type, maximum power output, and estimated charging time. These APIs are based on the Open Data Hub Mobility, which you can explore [here](https://swagger.opendatahub.com/?url=https://mobility.api.opendatahub.com/v2/apispec).

Please note that the availability of charging stations is dependent on the data provided by these APIs, which may be limited, especially outside the South Tyrol area.

#### Take a look to our slides [here](./presentation-slides.pdf)

## Accessing the Web Application
You can access the PowerNap website from both your mobile device and computer at: [https://ev-power-nap.vercel.app/map](https://ev-power-nap.vercel.app/map)

## API Endpoints

You can test our APIs at [https://powernap.alberto.fun/{endpoint}](https://powernap.alberto.fun/{endpoint}), replacing `{endpoint}` with one of the following:

- **GET** `/get-charging-station/?longitude=LONGITUDE&latitude=LATITUDE`
  - Retrieves stations within a 2km radius.

- **POST** `/get-locations/`
  - Returns coordinates based on an address provided in JSON format in the request body.
  - Example: `{"address": "Via Milano, 5 Bolzano"}`

- **GET** `/get-details-from-stations/?longitude=LONGITUDE&latitude=LATITUDE&current_battery=CURRENT_PERCENTAGE&desired_battery=DESIRED_PERCENTAGE&station_id=STATION_ID`
  - Retrieves details for a specific station identified by `station_id` from the `/get-charging-station` endpoint.

## Installation

To build the application locally and contribute to the codebase, you can open a pull request. The process is straightforward:

Install the dependencies:
```bash
yarn
# or
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
npm run dev
```

### Authors

<a href="https://www.linkedin.com/in/nicolo-menarbin" target="_blank">
  <img src="https://img.shields.io/badge/Nicolò%20Menarbin-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Nicolò Menarbin">
</a>

<a href="https://www.linkedin.com/in/alberto-crescini" target="_blank">
  <img src="https://img.shields.io/badge/Alberto%20Crescini-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Alberto Crescini">
</a>

<a href="https://www.linkedin.com/in/federico-bartsch" target="_blank">
  <img src="https://img.shields.io/badge/Federico%20Bartsch-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Federico Bartsch">
</a>
