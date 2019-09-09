const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '../dist'),
  assetsDir: 'static',
  publicPath: '/',
  // for prod, set publicPath to cdn set to 'domain.com/static'
};
