const path = require('path');
const webpack = require('webpack');

const TerserPlugin = require('terser-webpack-plugin');

// Get local IP Address
let os = require('os');
let interfaces = os.networkInterfaces();
let addresses = [];
for (let k in interfaces) {
    for (let k2 in interfaces[k]) {
      let address = interfaces[k][k2];
      if (address.family === 'IPv4' && !address.internal) {
            addresses.push(address.address);
        }
    }
}

ip_address = addresses[0]

// take debug mode from the environment
const debug = (process.env.NODE_ENV !== 'production');
const hashType = debug ? '[hash]': '[contentHash]'
const rootAssetPath = path.join(__dirname, 'assets');
let publicHost

if (ip_address !== undefined) {
    publicHost = debug ? 'http://' + ip_address + ':2992' : '';
}
else {
    publicHost = debug ? 'http://0.0.0.0:2992' : '';
}

if (ip_address !== undefined) {
    publicHost = debug ? 'http://' + ip_address + ':2992' : '';
}
else {
    publicHost = debug ? 'http://0.0.0.0:2992' : '';
}

module.exports = {
  // configuration
  context: __dirname,
  entry: {
    main_js: path.join(__dirname, 'assets', 'js', 'constructor.js'),
    /*main_css: [
      path.join(__dirname, 'assets', 'css', 'main.css'),
    ],*/
  },
  output: {
    path: path.resolve(__dirname, 'questmaker', 'static'),
    publicPath: `${publicHost}/static/`,
    filename: "script/[name]." + hashType + ".js",
    chunkFilename: "script/[name]." + hashType + ".chunk.js"
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        test: /\.js(\?.*)?$/i,
      }),
    ],
  },
}