# Icarus Web Application

## Installation Guide for Icarus 1.0
### Pre-Requisites

You must have Yarn installed before proceeding. See https://yarnpkg.com/lang/en/docs/install/

### Download

Download the following repository: https://github.com/SAR-Junior-Design/Front-End

### Dependencies and Installation

All dependencies are listed in the package.json file. To install these dependencies, launch a Terminal window, and change to the root directory of the vue project (demo-drone-app/). Then run the following code:

``` bash
yarn install
```

For more information on [vue-loader], visit http://vuejs.github.io/vue-loader

### Config

You will need to add a new file called `icarus-web-app/src/config/env.js` to the root of this directory.
The file should have the following format.

```
export default{
  base_url: '<url>',
  client_id: '<a character string key',
  client_secret: '<another character string key>'
}
```

### Build and Run

``` bash
# serve with hot reload at localhost:8080
yarn start

# build for production with minification
yarn run build
```

Open a web browser and in the Address Field go to the following

``` bash
localhost:8080
```

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
Check you are in the right directory (demo-drone-app) and try again.

<li> If the build is crashing the cloud instance, then, your cloud instance is too small. Try to build the instance locally.

</ul>

## Release Notes for Icarus 1.0
### New Features

<ul>
  <li>Added video background on Landing/Login pages.</li>
  <li>User can now upload and view documents on License page.</li>
  <li>User can upload profile picture on Settings.</li>
  <li>Polygons can now be deleted on both New Mission and Map page.</li>
  <li>Missions can now be identified by type (recreational, research, commercial)</li>
  <li>Tabs now disnguish between active and past missions on Home page</li>
  <li>No missions now directs to new mission if clicked</li>
  <li>Missions can now be filtered on Mission page</li>
  <li>Can delete drones on Drone Page</li>
  <li>Added descriptions to drones on Drone paged</li>
</ul> 

### Bug Fixes

<ul>
  <li>Pdfs uploaded in License page can be viewed.</li>
  <li>Navigation bar no longer disappears when window resizes for some browsers.</li>
  <li>Time and Date can updated if flight details are edited on Map page.</li>
  <li>Clicking outside of a picker no longer closes nav bar</li>
  <li>Fixed mission card formatting on Home page for consistency</li>
  <li>Fixed form so as not to give errors when empty after adding drone on Drone page</li>
  <li>Fixed add drone, so that only one drone is added at a time and not the entire table on Drone page</li>
  <li>When removing drone, it now only selects one drone instead of all on Drone page</li>
</ul>

### Known Bugs

<ul>
  <li>Uploaded documents under the License Page is not saved to the server.</li>
  <li>Updating profile picture under Settings does not save it to the server.</li>
  <li>Inactive drones on Map Page show data as null.</li>
  <li>User cannot remove a drone from a mission once added on Map Page.</li>
  <li>Tabs on home page are dynamically sizing, making Home page jittering</li>
  <li>Home page is bloated and slow due to API calls and calcultaions</li>
  <li>Mini map component breaks if multiple polygons are drawn in a single mission</li>
  <li>Cursor stays crosshair, if user leaves while drawing area</li>
</ul> 
