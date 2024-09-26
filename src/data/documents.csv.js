import { csv } from "d3-fetch";
import { csvFormat } from "d3-dsv";

const pgp_documents_csv =
  "https://raw.githubusercontent.com/princetongenizalab/pgp-metadata/main/data/documents.csv";

async function pgp_documents() {
  const documents = await csv(pgp_documents_csv);
  // TODO: error handling
  // if (!response.ok) throw new Error(`fetch failed: ${response.status}`);

  // load pgp documents and populate unset/empty type as "Unknown"
  //
  return documents.map((info) => {
    info.type = info.type || "Unknown";
    return info;
  });
}

// import { csvFormat } from "d3-dsv";

// // Fetch GeoJSON from the USGS.
// const response = await fetch(
//   "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson",
// );
// if (!response.ok) throw new Error(`fetch failed: ${response.status}`);
// const collection = await response.json();

// // Convert to an array of objects.
// const features = collection.features.map((f) => ({
//   magnitude: f.properties.mag,
//   longitude: f.geometry.coordinates[0],
//   latitude: f.geometry.coordinates[1],
// }));

const documents = await pgp_documents();
//process.stdout.write(JSON.stringify(documents));

// Output CSV.
process.stdout.write(csvFormat(documents));

// // async function json(url) {
// //   const response = await fetch(url);
// //   if (!response.ok) throw new Error(`fetch failed: ${response.status}`);
// //   return await response.json();
// // }

// // const station = await json(`https://api.weather.gov/points/${latitude},${longitude}`);
// // const forecast = await json(station.properties.forecastHourly);

// process.stdout.write(JSON.stringify(documents));
