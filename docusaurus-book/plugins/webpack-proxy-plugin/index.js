// docusaurus-book/plugins/webpack-proxy-plugin/index.js
module.exports = function (context, options) {
  return {
    name: "webpack-proxy-plugin",
    configureWebpack(config, isServer, utils) {
      return {
        mergeStrategy: { "devServer.proxy": "replace" },
        devServer: {
          proxy: [
            {
              context: ["/api/auth/login"], // More specific rule first
              target: "http://localhost:8000", // Point login to FastAPI
              secure: false,
              changeOrigin: true,
              logLevel: "debug",
            },
            {
              context: ["/api/auth"], // General rule for other /api/auth routes
              target: "http://localhost:8001", // Point others to better-auth
              secure: false,
              changeOrigin: true,
              logLevel: "debug",
            },
          ],
        },
      };
    },
  };
};
