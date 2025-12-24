/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI Humanoid Book',
  url: 'https://Ameen-0099.github.io',
  baseUrl: '/humanoid-robotics-book/',
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.ico',
  organizationName: 'Ameen-0099', // Usually your GitHub org/user name.
  projectName: 'humanoid-robotics-book', // Usually your repo name.

  customFields: {
    apiBaseUrl: 'http://localhost:8000',
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/Ameen-0099/humanoid-robotics-book/tree/main/',
        },

        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    './plugins/webpack-proxy-plugin', // Path to your plugin
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
          {
            to: '/',
            from: ['/docs', '/docs/intro'],
          },
        ],
      },
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
            navbar: {
              title: 'AI Humanoid Book',
      
                      logo: {
                        alt: 'AI Humanoid Robotics Logo',
                        src: 'img/new_logo.png',
                      },              items: [
      
                {
                  type: 'doc',
                  docId: 'intro',
                  position: 'left',
                  label: 'Tutorial',
                },
      
                {
                  href: 'https://github.com/Ameen-0099/humanoid-robotics-book',
                  label: 'GitHub',
                  position: 'right',
                },
                {
                  type: 'custom-AuthNavbarItem',
                  position: 'right',
                  className: 'auth-navbar-item',
                },

              ],
            },
            algolia: {
              // The application ID provided by Algolia
              appId: 'YOUR_APP_ID',
      
              // Public API key: it is safe to commit it
              apiKey: 'YOUR_SEARCH_API_KEY',
      
              indexName: 'YOUR_INDEX_NAME',
      
              // Optional: see doc section below
              contextualSearch: true,
      
              // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
              externalUrlRegex: 'external\\.com|domain\\.com',
      
              // Optional: Replace parts of the item URLs from Algolia. Useful when using the same search index for multiple deployments using a different baseUrl. You can use regexp or string in the `from` param. For example: localhost:3000 vs myCompany.com/docs
              replaceSearchResultPathname: {
                from: '/docs/', // or as RegExp: /\/docs\//
                to: '/',
              },
      
              // Optional: Algolia search parameters
              searchParameters: {},
      
              // Optional: path for search page that enabled by default (`false` to disable)
              searchPagePath: 'search',
            },
            footer: {
        style: 'dark',
        links: [
          {
            title: 'Docs',
            items: [
              { label: 'Introduction', to: '/intro' },
              { label: 'Foundations', to: '/foundations' },
              { label: 'ROS', to: '/ros' },
              { label: 'Simulation', to: '/simulation' },
              { label: 'Isaac', to: '/isaac' },
              { label: 'VLA', to: '/vla' },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/docusaurus',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/docusaurus',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/docusaurus',
              },
            ],
          },
          {
            title: 'More',
            items: [
              { label: 'Kinematics', to: '/kinematics' },
              { label: 'Manipulation', to: '/manipulation' },
              { label: 'GPT', to: '/gpt' },
              { label: 'Learning', to: '/learning' },
              { label: 'Ethics', to: '/ethics' },
              { label: 'Locomotion', to: '/locomotion' },
              { label: 'Capstone', to: '/capstone' },
              { label: 'References', to: '/references' },
              {
                label: 'GitHub',
                href: 'https://github.com/Ameen-0099/humanoid-robotics-book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
      },

    }),
};

module.exports = config;