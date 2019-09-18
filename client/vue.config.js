const path = require('path');

module.exports = {
  outputDir: path.resolve(__dirname, '../static'),
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/'
    : '/',
};
