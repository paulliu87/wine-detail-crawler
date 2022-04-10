const axios = require('axios');
const WINE_BASE_URL = 'https://www.wine-searcher.com';
const utils = require('./utils');

let client = {};

const returnHtml = ({ data, error }) => error ? null : data;
const onError = (error, errorMsg) =>
  console.error(`${errorMsg} Error: ${error.response.status}, ${error.response.statusText}`);
const fetchWineWeb = (path) => {
  const url = `${WINE_BASE_URL}${path}`;
  const headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
  };
  return axios.get(url, { headers });
};

client.getRegionDetails = (context = {}, parser) =>
  fetchWineWeb('/regions')
    .then(returnHtml)
    .then(parser)
    .catch((error) =>
      onError(error, 'Failed to fetch regions and subregions.')
    );

client.getWineUrls = (context = {}, requestParams, parser) => {
  const { country } = requestParams;
  return fetchWineWeb(`/regions-${country}`)
    .then(returnHtml)
    .then(parser)
    .catch((error) =>
      onError(error, `Failed to fetch wine urls, region: ${region}, subregion: ${subregion}.`)
    );
}

client.getWineDetailsByRegion = (context = {}, requestParams, parser) => {
  const { url } = requestParams;
  return fetchWineWeb(url)
    .then(returnHtml)
    .then(parser)
    .catch((error) =>
      onError(error, `Failed to fetch wine information, url: ${url}.`)
    );
}

module.exports = client;