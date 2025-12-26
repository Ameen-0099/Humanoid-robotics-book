// docusaurus-book/plugins/webpack-proxy-plugin/index.js
module.exports = function (context, options) {
  return {
    name: 'docusaurus-plugin-proxy',
    configureWebpack(config, isServer, utils) {
      return {
        devServer: {
          proxy: [
            {
              context: ['/api'],
              target: 'http://localhost:8000',
              pathRewrite: { '^/api': '' },
              secure: false,
              changeOrigin: true,
              logLevel: 'debug',
            },
          ],
        },
      };
    },
  };
};
