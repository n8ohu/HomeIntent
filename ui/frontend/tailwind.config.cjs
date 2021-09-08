const config = {
	mode: "jit",
	purge: [
		"./src/**/*.{html,js,svelte,ts}",
	],
	theme: {
		extend: {
		     colors: {
        		'hi-green': '#43ae4f',
      		}
		},
	},
	plugins: [],
};

module.exports = config;