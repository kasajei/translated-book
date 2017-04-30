var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var config = require('./webpack.config.js');

config.output.path = require('path').resolve('./static/dist');

config.plugins = config.plugins.concat([
    new BundleTracker({filename: './webpack-stats-prod.json'}),

    // removes a lot of debugging code in React
    new webpack.DefinePlugin({
        'process.env': {
            'NODE_ENV': JSON.stringify('production')
        }
    }),

    new webpack.optimize.OccurrenceOrderPlugin(true),

  // minifies your code
    new webpack.optimize.UglifyJsPlugin({
        compressor: {
        warnings: false
        }
    })
]);

module.exports = config;
