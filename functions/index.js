const functions = require('firebase-functions');
const { Nuxt } = require('nuxt');

const config = {
  dev: false,
  buildDir: 'nuxt',
  build: {
    publicPath: '/app/static/'
  }
};
const nuxt = new Nuxt(config);

exports.app = functions.https.onRequest((req, res) => {
  nuxt.render(req, res);
});
