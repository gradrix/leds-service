const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const { promises: fs } = require('fs')
const readline = require('readline');
const path = require('path');

function askForBuildDestination(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans);
    }))
}

// async function getBuildDestinationPath() {
//     const filePath = __dirname + "/settings.cfg";
//     return fs.access(filePath, fs.F_OK)
//         .then(async () => {
//             const result = await fs.readFile(filePath, (error, data) => {
//                 if(error) {
//                     throw error;
//                 }
//                 return data;
//             })
//             return result.toString();
//         })
//         .catch(async () => {
//             const buildDestination = await askForBuildDestination("Please type destination path (absolute) - e.g.: '/home/g/repos/leds-service/frontend-build':\n");
//             return await fs.access(buildDestination, fs.F_OK)
//                 .then(async () => {
//                     const destination = buildDestination.replace(/(\r\n|\n|\r)/gm, "");
//                     return fs.writeFile(filePath, destination)
//                         .then(() => destination)
//                         .catch((err) => {
//                             console.log(err);
//                         });
//                 })
//                 .catch((error) => {
//                     throw new Error("Invalid path specified.. "+error);
//                 });
//         })      
// }

async function getBuildDestinationPath() {
    return __dirname + "/build";
}

module.exports = async (env, argv) => {
  const isDevMode = argv.mode === "development";
  const sourceMapOptions = {
    sourceMap: isDevMode
  };
  return await getBuildDestinationPath()
    .then(buildDestination => {
        console.log("Building source to: "+buildDestination);
        return {
            entry: "./index.js",
            output: {
                path: buildDestination,
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
            performance: {
                hints: false,
                maxEntrypointSize: 512000,
                maxAssetSize: 512000
            }
          }        
    })
}
