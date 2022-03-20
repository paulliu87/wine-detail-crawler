let utils = {};

utils.formatCountryName = (countryName) =>
  countryName ? countryName.replaceAll(' ', '-').toLowerCase() : countryName;

utils.buildProfilePath = (path) => path.replaceAll('/1/any', '#t2');

module.exports = utils;