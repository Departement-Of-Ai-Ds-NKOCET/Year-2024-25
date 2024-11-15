const path = require('path');

module.exports = {
  entry: './popup.js', // Update if your entry point is different
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  resolve: {
    extensions: ['.js', '.json', '.wasm'],
  },
};
