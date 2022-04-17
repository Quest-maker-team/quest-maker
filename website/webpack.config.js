const path = require('path');
const webpack = require('webpack');

const TerserPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const { CleanWebpackPlugin }  = require('clean-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

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
const hashType = debug ? '[hash]': '[contentHash]';
console.log(debug);
let publicHost

if (ip_address !== undefined) {
    publicHost = debug ? 'http://' + ip_address + ':2992' : '';
}
else {
    publicHost = debug ? 'http://0.0.0.0:2992' : '';
}

module.exports = {
  // configuration
  // watch: true,
  mode: debug ? 'development' : 'production',
  context: __dirname,
  entry: {
    main_js: path.join(__dirname, 'assets', 'js', 'constructor.js'),
  },
  output: {
    path: path.resolve(__dirname, 'questmaker', 'static'),
    publicPath: `${publicHost}/static/`,
    filename: "js/[name]." + hashType + ".js",
    chunkFilename: "js/[name]." + hashType + ".chunk.js"
  },
  optimization: {
    // minimize: true,
    minimizer: [
      new CssMinimizerPlugin(),
      new TerserPlugin({
        test: /\.js(\?.*)?$/i,
      }),
    ],
  },
  module: {
    rules: [
        {
          test: /\.js$/,
          //exclude: /node_modules/,
          use: 'babel-loader',
        },
        {
          test: /\.(?:ico|gif|png|jpg|jpeg|svg|woff(2)?|eot|ttf|otf)$/i,
          use: [
            {
              loader: 'file-loader',
              options: {
                name: '[folder]/[name].' + hashType + '.[ext]',
              },
            },
          ],
        },
        {
            test: /\.(scss|css)$/,
            use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader'],
        },
    ],
  },
  plugins: [
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: [
        '*',
        '!manifest.json',
    ],
    }),
    new MiniCssExtractPlugin({ filename: 'css/[name].' + hashType + '.css', }),
    new WebpackManifestPlugin({ publicPath:"/static/" }),
  ],
}