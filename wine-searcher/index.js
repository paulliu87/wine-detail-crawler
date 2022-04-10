const client = require('./src/wineWebClient');
const parser = require('./src/htmlParser');
const utils = require('./src/utils');
const fs = require('fs')
// query for product and tab 2 for profile

const main = async () => {
  let result = {};
  // get all region and subregion data
  const regionDetails = await client.getRegionDetails({}, parser.regionDetails);
  // TODO: all 20 pages, increamen 1 + 25 * index
  let wineLinks = {};
  for (let [continentName, countries] of Object.entries(regionDetails)) {
    countries.forEach(async ({ country }, index) => {
      if (country && index === 0) {
        const formatedCountryName = utils.formatCountryName(country);
        console.log({ formatedCountryName })
        wineLinks[formatedCountryName] = await client.getWineUrls(
          {}, { country: formatedCountryName }, parser.wineLinks
        );
      }
    })
  }
  wineLinks.forEach(async (link) => {
    const crtInfo = client.getWineDetailsByRegion(
      {},
      { url: utils.buildProfilePath(link) },
      parser.wineDetails
    );
    result = { ...result, ...crtInfo };
  })
  
  const outputFile = '/Users/moriaty/src/Learning/ml/wine/wine-and-pair-food-crawler/resource/data.txt';
  console.log(`^^^^^^^^ Write final result to local file: ${outputFile} ^^^^^^^^`)
  await fs.writeFile(outputFile, result, err => {
    if (err) {
      console.error(err)
      return;
    }
    console.log('File is written successfully.');
  });
}
main();