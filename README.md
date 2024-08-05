# PowerNap - EV Charging Stations Finder

Web/Mobile application to find the best EV charger based on distance from the destination, time of stay, charger speed, electricity costs, current battery level, and the desired one.

The algorithm uses a heuristic that allows calculating a score for each station as a weighted combination of some relevant information.

Our public APIs offer an easy way to access useful information such as walking distance from the station to the destination, station location, charging costs, provider, socket type, maximum power output, and expected charging time.

You can test out our APIs at [https://powernap.alberto.fun/{endpoint}](https://powernap.alberto.fun/{endpoint})

where `{endpoint}` is one of the following:

### API Endpoints

- **GET** `/get-charging-station/?longitude={xx}&latitude={yy}` 
  - Returns stations within a 2km radius

- **GET** `/get-locations/` 
  - Returns a set of coordinates based on an address passed in JSON format in the body 
  - Example: `{"address": "Via Milano, 5 Bolzano"}`

- **GET** `/get-details-from-stations/?longitude={xx}&latitude={yy}&current_battery={cc}&desired_battery={bb}&station_id={aa}` 
  - Where station id is one of the several retrieved from the `/get-charging-station` endpoint

## Install the dependencies
```bash
yarn
# or
npm install
```

### Start the app in development mode (hot-code reloading, error reporting, etc.)
```bash
npm run dev
```

### Lint the files
```bash
yarn lint
# or
npm run lint
```

### Format the files
```bash
yarn format
# or
npm run format
```

### Build the app for production
```bash
npm run build
```

### Customize the configuration
See [Configuring quasar.config.js](https://v2.quasar.dev/quasar-cli-vite/quasar-config-js).

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
