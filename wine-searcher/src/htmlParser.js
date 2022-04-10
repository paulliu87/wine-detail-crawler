let cheerio = require('cheerio');
let parser = {};

parser.regionDetails = (html) => {
  let $ = cheerio.load(html);
  let regions = {}
  let continentName, country, description;
  $('.card-body.p-3.p-sm-4').each((i, ref) => {
    continentName = $(ref).children('h2').text();
    if (continentName && !['Others', 'Signature Regional Styles'].includes(continentName)) {
      const countries = [];
      $(ref).find('h5.card-title').each((j, subref) => {
        country = $(subref).text();
        description = $(subref).siblings('p').text();
        countries.push({ country, description });
      })
      regions[continentName] = countries;
    }
  });
  return regions;
}

parser.wineLinks = (html) => {
  let $ = cheerio.load(html);

  let links = [];
  $('tr.row.mx-0 a.superlative-list__name.font-light-bold').each((i, ref) => {
    links.push($(ref).attr('href'));
  })
  return links;
}

parser.wineDetails = (html) => {
  let $ = cheerio.load(html);

  let wine = {};
  const wineName = $('.product-details__container-right.d-flex.flex-column.mt-4A.mt-md-0.pl-0.mb-0 h1').text().trim();
  const info = $('div.learn-more-list__item .learn-more-list__item-content').each((i, ref) => {
    let str = '';
    str = str + ',' + $(ref).text();
  })
  wine[wineName] = str;
  return wine;
}

module.exports = parser;