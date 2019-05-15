# Flyright Web Application

## Installation Guide for Icarus 1.0
### Pre-Requisites

First install the nvm. This code works with node v8 but I have not done extensive testing on more recent versions.

You can install the node version manager (NVM) like this: `wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash`

Also refer to the NVM github here: (https://github.com/nvm-sh/nvm)[https://github.com/nvm-sh/nvm]

You will need to exit and reopen the terminal to get nvm to work after installation.

Then install node v8: `nvm install v8`

And finally to use v8, type `nvm use v8`

You must have Yarn installed before proceeding. See (https://yarnpkg.com/lang/en/docs/install/)[https://yarnpkg.com/lang/en/docs/install/] for information on installation.

### Dependencies and Installation

All dependencies are listed in the package.json file. To install these dependencies, launch a Terminal window, and change to the root directory of the vue project (demo-drone-app/). Then run the following code:

``` bash
yarn install
```

For more information on [vue-loader], visit http://vuejs.github.io/vue-loader

### Config

You will need to add a new file called `icarus-web-app/src/config/env.js` to the root of this directory. This is *not* the config folder `icarus-web-app/config`, that is a different location and if you put your `env.js` file there it will not work.
The file should have the following format.

```
export default{
  base_url: '<url>',
  client_id: '<a character string key',
  client_secret: '<another character string key>'
}
```

### Build and Run

ATTENTION: Make sure you have your env.js file setup or else the website will not run.

``` bash
# serve with hot reload at localhost:8080
yarn start

# build for production with minification
yarn build
```

Open a web browser and in the Address Field go to the following

``` bash
localhost:8080
```

If you want to run on the server, setup nginx. Upload the `dist/` folder that is
generated when `yarn build` is run. Setup the nginx enabled-site to point to the
index.html file in the `dist` to statically serve the webapp.

### Troubleshooting

<ul>

<li> If you recieve the following after yarn install:

``` bash
yarn install v1.1.0
info No lockfile found.
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...

info Lockfile not saved, no dependencies.
```
Check you are in the right directory (icarus-web-app) and try again.

<li> If the build is crashing the cloud instance, then, your cloud instance is too small. Try to build the instance locally.

</ul>
