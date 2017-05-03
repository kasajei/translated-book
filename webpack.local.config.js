var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var config = require('./webpack.config.js');

config.entry = config.entry.concat([
    'webpack-dev-server/client?http://localhost:3000',
    'webpack/hot/only-dev-server'
]);

config.devtool = 'inline-source-map';

config.devServer = {
    publicPath: "/assets/bundles/",
    contentBase: "./assets/",
    host: 'localhost',
    port: 3000,
    historyApiFallback: true,
    hot: true,
    inline: true
};

config.output.publicPath = 'http://localhost:3000/assets/bundles/';

delete config.module.loaders[0].loader;
delete config.module.loaders[0].query;
config.module.loaders[0].loaders = ['react-hot-loader', 'babel-loader?presets[]=es2015,presets[]=react'];


config.plugins = config.plugins.concat([
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NamedModulesPlugin(),
    new webpack.NoEmitOnErrorsPlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('local')
      }
    })
]);

module.exports = config;
