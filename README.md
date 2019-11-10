# FlyRight
A drone flight registration system to help local law enforcement. This system is currently used by GTPD at the Georgia Institute of Technology. 

I have been working for the past year and a half with the Georgia Tech Police Department to develop and deploy this system. Though they do not have jurisdiction to control their airspace, the ability to review and communicate with pilots has been invaluable: during the super bowl there were 64 TFR (Temporary Flight Restriction) infractions across Atlanta, costing each pilot roughly $20,000 and over $1 million in total. None came from Georgia Tech campus. Using our software, all pilots were notified with the email functionality and all flight plans were recommended against. This way we ensured a safer campus.

![](https://raw.githubusercontent.com/samcrane8/FlyRight/master/docs/flight_page.png)

![](https://raw.githubusercontent.com/samcrane8/FlyRight/master/docs/flights_page.png)

## Videos

- Flight registration demonstration: https://www.youtube.com/watch?v=AOCtnlbaQSA&feature=youtu.be
- Docker Setup Tutorial: https://youtu.be/4RKAR-1bODA
- Using Postman with FlyRight: https://www.youtube.com/watch?v=i7WmmnFCjUw&list=PLUUN7t5qIozu7Z-5AWewMwrVWcxL0QBaY&index=3
- Setting up Departments: https://youtu.be/82ST8Z8BgJU

## Setup

(Dev) Setup has become lightning fast with the new docker-compose scripts. We also have a "prod" deployment script that is used by GTPD and can be the inspiration for other deployments.

### Docker and Docker-Compose

To work with this codebase you will need docker: https://docs.docker.com/install/

If you have not used docker before, it makes code deployment infinitely easier by putting your code into "containers", allowing
you to make sure that everytime you deploy code the environment is the same. It also makes it easy to do everything in one line.

As well, you will need docker-compose: https://docs.docker.com/compose/install/

Docker-Compose takes it one step further: it allows you to orchestrate many containers together in one deployment.

### Build

Once you have docker and docker-compose installed, the rest is pretty straightforward.

First you are going to want to navigate to the webapp directory and run: `yarn install`

Then return the root, and run this command: `docker-compose up -d`

Note: docker-compose up only builds new container images if there is not one there already. if you want to force it to rebuild, run it with
this flag: `docker-compose up -d --build`

The one command above is enough to get everything setup. Just wait a bit as everything installs.

Now, if you want to take it down, type this command: `docker-compose down`

And if you want to delete the volumes created with it, run it with this flag: `docker-compose down -v`

And that is it! Hot reloading works with these containers, so as you change code in your IDE, the containers will update (the caveat being some changes will require you to restart the server, like changes to the process.env values in the webapp server, but 99% of them can use hot reloading)

## API

Currently we do not have a postman workspace because we are cheap. However if you download the postman collection and environment variables you can interact with the API from postman.

We also have a readme with endpoint details [here](https://github.com/samcrane8/FlyRight/tree/master/docs). We generate the documents with a project called [Postdown](https://github.com/TitorX/Postdown). The only issue is that Postdown does not currently handle Folders nor empty description/queries properly, so I had to fork the repo. I have a pull request waiting but in the meantime, you can use my fork [here](https://github.com/samcrane8/Postdown).

## Partners

[Georgia Tech Police Department](http://www.police.gatech.edu/) was critical in the development of this system. The original IcarusMap project was with head of Physical Security, Jeffrey Hunnicutt, who met with our team weekly to hone this product to best help the campus.

## Contributors

### How to Help

If you would like to help, please send me an email (samcrane8@gmail.com) with the subject line starting with [FlyRight]. I also have not maintained a large open-sourced repository before so guidance on that front would be appreciated as well. Here are the things I would like to accomplish:

#### To Do

<ul>
  <li> [x] Docker container setup scripts.
  <li> [ ] Unit Testing on the Front-End
  <li> [ ] Comprehensive unit-testing on the back-end server.
  <li> [ ] iOS app implementation.
  <li> [ ] airspace deconfliction
  <li> [ ] 3D flight plans
  <li> [ ] Setup watchdog to restart celery-worker if it ever crashes.
</ul>

### Initial Team

This codebase started as a junior design project at Georgia Tech. The original version was called IcarusMap.

The team involved was the following:

Kaan Göksal - https://github.com/kaangoksal

Antonia Deliyianni - https://github.com/adeliyianni3

Raymond Zhang - https://github.com/rzhang339

Timothy Lee O'Connor - https://github.com/tjlo3

Ladd Jones - https://github.com/laddjones

Though this project has jumped different repositories and it does not show in the git history, these people were involved at the beginning and deserve credit.

### Pelori

Sam Crane and Kaan Göksal subsequently founded [Pelori](http://www.pelori.io) as a computer vision provider for public safety. Pelori provides deployment and server maintenance solutions, and is a major contributor to the FlyRight source code.
