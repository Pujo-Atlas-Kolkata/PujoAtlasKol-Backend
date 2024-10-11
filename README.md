<!-- <p align="center">
  <a href="http://nestjs.com/" target="blank"><img src="https://nestjs.com/img/logo-small.svg" width="120" alt="Nest Logo" /></a>
</p>

[circleci-image]: https://img.shields.io/circleci/build/github/nestjs/nest/master?token=abc123def456
[circleci-url]: https://circleci.com/gh/nestjs/nest

  <p align="center">A progressive <a href="http://nodejs.org" target="_blank">Node.js</a> framework for building efficient and scalable server-side applications.</p>
    <p align="center">
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/v/@nestjs/core.svg" alt="NPM Version" /></a>
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/l/@nestjs/core.svg" alt="Package License" /></a>
<a href="https://www.npmjs.com/~nestjscore" target="_blank"><img src="https://img.shields.io/npm/dm/@nestjs/common.svg" alt="NPM Downloads" /></a>
<a href="https://circleci.com/gh/nestjs/nest" target="_blank"><img src="https://img.shields.io/circleci/build/github/nestjs/nest/master" alt="CircleCI" /></a>
<a href="https://coveralls.io/github/nestjs/nest?branch=master" target="_blank"><img src="https://coveralls.io/repos/github/nestjs/nest/badge.svg?branch=master#9" alt="Coverage" /></a>
<a href="https://discord.gg/G7Qnnhy" target="_blank"><img src="https://img.shields.io/badge/discord-online-brightgreen.svg" alt="Discord"/></a>
<a href="https://opencollective.com/nest#backer" target="_blank"><img src="https://opencollective.com/nest/backers/badge.svg" alt="Backers on Open Collective" /></a>
<a href="https://opencollective.com/nest#sponsor" target="_blank"><img src="https://opencollective.com/nest/sponsors/badge.svg" alt="Sponsors on Open Collective" /></a>
  <a href="https://paypal.me/kamilmysliwiec" target="_blank"><img src="https://img.shields.io/badge/Donate-PayPal-ff3f59.svg" alt="Donate us"/></a>
    <a href="https://opencollective.com/nest#sponsor"  target="_blank"><img src="https://img.shields.io/badge/Support%20us-Open%20Collective-41B883.svg" alt="Support us"></a>
  <a href="https://twitter.com/nestframework" target="_blank"><img src="https://img.shields.io/twitter/follow/nestframework.svg?style=social&label=Follow" alt="Follow us on Twitter"></a>
</p> -->
  <!--[![Backers on Open Collective](https://opencollective.com/nest/backers/badge.svg)](https://opencollective.com/nest#backer)
  [![Sponsors on Open Collective](https://opencollective.com/nest/sponsors/badge.svg)](https://opencollective.com/nest#sponsor)-->

# Project Setup and Running Guide

This guide will walk you through the steps required to set up and run the project using Taskfile. Make sure you have all the prerequisites installed before proceeding.

## Prerequisites

Before you start, ensure that the following software is installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/)
- [Nest.js](https://docs.nestjs.com/first-steps)

You can check if these tools are installed by running the following commands:

```sh
docker --version
docker-compose --version
node --version
npm --version
```

## Setup

We are using nest js for our backend, so please install nest js globally in your system.

```sh
   npm i -g @nestjs/cli
```

### Steps to Set Up

1. Clone the repository:

   ```sh
   git clone https://github.com/Pujo-Atlas-Kolkata/PujoAtlasKol-Backend.git
   cd PujoAtlasKol-Backend
   ```

2. Install all the dependencies:

   ```sh
   npm install
   ```

3. Run the Application detached:

   ```sh
      npm run start
   ```

### Validate Application Status

- Server

```sh
   localhost:3000
```

## Troubleshooting

- **Docker Not Running**: Ensure Docker is running before starting the setup.
- **Port Conflicts**: If any port conflicts occur, make sure no other services are running on the required ports.

## Contributing

We 💖 contributors! Feel free to contribute to this project but **please read the [Contributing Guidelines](CONTRIBUTING.md) before opening an issue or PR** so you understand the branching strategy. We also welcome you to join our [Discord](https://discord.com/invite/xxSXWYf6d4) community for either support or contributing guidance.

![Alt](https://repobeats.axiom.co/api/embed/e21736ab847e9d6aaf62bbd15061f5793f087dff.svg 'Repobeats analytics image')

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Sponsors

A special thank you to **Netlify**, **Cloudflare**, and **Sentry** for sponsoring **Pujo Atlas**!

<div>
   <a href="https://www.netlify.com" target="_blank" rel="noopener noreferrer"><img src="https://www.netlify.com/v3/img/components/netlify-color-accent.svg" alt="Deploys by Netlify" /></a>
   <a href="https://www.cloudflare.com" target="_blank" rel="noopener noreferrer"><img src="https://cf-assets.www.cloudflare.com/slt3lc6tev37/CHOl0sUhrumCxOXfRotGt/081f81d52274080b2d026fdf163e3009/cloudflare-icon-color_3x.png" alt="Cloudflare Badge" height="50px" width="100px" /></a>
   <a href="https://www.sentry.io" target="_blank" rel="noopener noreferrer"><img src="https://avatars.githubusercontent.com/u/1396951?v=4" alt="Cloudflare Badge" height="50px" width="50px" /></a>
</div>
