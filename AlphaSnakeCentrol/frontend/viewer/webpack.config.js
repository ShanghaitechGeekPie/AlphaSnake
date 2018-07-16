module.exports = {
	mode: "production",

	entry: __dirname + "/src/main.js",
	output: {
		path: __dirname + "/public",
		filename: "bundle.js"
	},

	devtool: "eval-source-map",

	devServer: {
		contentBase: __dirname + "/public",
		historyApiFallback: false,
		inline: true
	},

	module: {
		rules: [
			{
				test: /(\.js)$/,
				use: {
					loader: "babel-loader"
				},
				exclude: /node_modules/
			}
		]
	}
};