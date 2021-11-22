const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const path = require('path');

module.exports = (env, argv) => {
  var currentPath = __dirname;
  const isDevMode = argv.mode === "development";
  const sourceMapOptions = {
    sourceMap: isDevMode
  };
  if (isDevMode) {
    currentPath = path.join(__dirname, '../backend');
  }

  return {
    entry: "./index.js",
    output: {
        path: currentPath + "/react-build",
        filename: "js/bundle.js",
        publicPath: "/content/"
    },
    module: {
        rules: [
            // Javascript
            {
                test: /\.(js|jsx)$/, 
                exclude: /node_modules/,
                loader: "babel-loader",
                options: {
                    presets: ["@babel/preset-env", "@babel/preset-react"]
                }                        
            },
            // Stylesheets
            {
                test: /\.(scss|css)$/,
                use: [
                    { loader: MiniCssExtractPlugin.loader }, 
                    { loader: "css-loader", options: sourceMapOptions },
                    { loader: "sass-loader", options: sourceMapOptions }
                ]
            },
            // Font Definitions
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [{
                    loader: "file-loader",
                    options: {
                        name: "[name].[ext]",
                        outputPath: "fonts/"
                    }
                }]
            },
            // Images
            { 
                test: /\.(gif|png)$/,  
                use: [{
                    loader: "file-loader",
                    options: {
                        name: "[name].[ext]",
                        outputPath: "images/"
                    }
                }]
            }
        ]
    },
    devtool: isDevMode ? "source-map" : false,
    plugins: [
        new HtmlWebpackPlugin({
            hash: true,
            title: "LEDS",
            template: "./index.html",
            filename: "index.html",
            favicon: "./img/favicon.ico"
        }),
        new MiniCssExtractPlugin({
            filename: "css/bundle.css"
        }),
        new BundleAnalyzerPlugin(),
        // Quit after build
        {
          apply: (compiler) => {
            compiler.hooks.done.tap("DonePlugin", (stats) => {
            console.log("Build is completed!");
            setTimeout(() => {
              if (!isDevMode) {
                process.exit(0);
              }
            });
          });
         }
        }
    ],
    watch: isDevMode,
  }
}
