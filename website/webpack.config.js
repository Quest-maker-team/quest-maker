const path = require('path');
const webpack = require('webpack');

const TerserPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const { CleanWebpackPlugin }  = require('clean-webpack-plugin');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const { IgnoreEmitPlugin } = require('ignore-emit-webpack-plugin');

// take debug mode from the environment
const debug = (process.env.NODE_ENV.trim() !== 'production');
const hashType = debug ? '[fullhash]': '[contenthash]';

module.exports = {
  // configuration
  watch: true,
  mode: debug ? 'development' : 'production',
  context: __dirname,
  entry: {
    constructor_js: path.join(__dirname, 'assets', 'js', 'constructor.js'),
    jquery_js: path.join(__dirname, 'assets', 'js', 'jquery','jquery.min.js'),
    bootstrap_js: path.join(__dirname, 'assets', 'js', 'bootstrap','bootstrap.bundle.min.js'),
    bootstrap_css: path.join(__dirname, 'assets', 'css', 'bootstrap','bootstrap.min.css'),
    index_css: path.join(__dirname, 'assets', 'css', 'index.css'),
    forms_css: path.join(__dirname, 'assets', 'css', 'forms.css'),
    roboto_css: path.join(__dirname, 'assets', 'css', 'roboto.css'),
    style_css: path.join(__dirname, 'assets', 'css', 'style.css'),
  },
  output: {
    path: path.resolve(__dirname, 'questmaker', 'static'),
    publicPath: '/static/',
    filename: "js/[name]." + hashType + ".js",
    chunkFilename: "js/[name]." + hashType + ".chunk.js",
    assetModuleFilename: 'fonts/[name][hash][ext]',
  },
  optimization: {
    minimizer: [
      new CssMinimizerPlugin({
        test: /\.css$/i,
        exclude: /bootstrap/,
      }),
      new TerserPlugin({
        test: /\.js$/i,
      }),
    ],
  },
  module: {
    rules: [
        {
          test: /\.js$/,
          use: 'babel-loader',
        },
        {
          test: /\.(?:ico|gif|png|jpg|jpeg|svg)$/i,
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
          test: /\.(woff|woff2|eot|ttf|otf)$/i,
          type: 'asset/resource',
        },
        {
            test: /\.(scss|css)$/,
            exclude: /bootstrap/,
            use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader', 'sass-loader'],
        },
        {
          test: /bootstrap[^\.]*(\.[^\.]*)*.css$/,
          use: [
            {
              loader: 'file-loader',
              options: {
                name: 'css/[name].' + hashType + '.css',
              },
            },
          ],
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
    new IgnoreEmitPlugin(/(?<=.*_css\s*).*?(?=\s*js)/gs),
    new MiniCssExtractPlugin({ filename: 'css/[name].' + hashType + '.css', }),
    new WebpackManifestPlugin({ publicPath:"/static/" }),
  ],
}