# FlyRight
A drone flight registration system to help local law enforcement. This system is currently used by GTPD at the Georgia Institute of Technology. 

I have been working for the past year and a half with the Georgia Tech Police Department to develop and deploy this system. Though they do not have jurisdiction to control their airspace, the ability to review and communicate with pilots has been invaluable: during the super bowl there were 64 TFR (Temporary Flight Restriction) infractions across Atlanta, costing each pilot roughly $20,000. None came from Georgia Tech campus. Using our software, all pilots were notified with the email functionality and all flight plans were recommended against. This way we ensured a safer campus.
Here is a video demonstration: [https://www.youtube.com/watch?v=AOCtnlbaQSA&feature=youtu.be](https://www.youtube.com/watch?v=AOCtnlbaQSA&feature=youtu.be)

![](https://raw.githubusercontent.com/samcrane8/FlyRight/master/docs/flight_page.png)

![](https://raw.githubusercontent.com/samcrane8/FlyRight/master/docs/flights_page.png)

## Setup

There are two major projects within this repository. The business-logic-server, and the webapplication.
The readmes in each folder will explain how to set up the respective projects. 

## API

Currently we do not have a postman workspace because we are cheap. We do have a readme with endpoint details [here](https://github.com/samcrane8/FlyRight/tree/master/docs). We generate the documents with a project called [Postdown](https://github.com/TitorX/Postdown). The only issue is that Postdown does not currently handle Folders nor empty description/queries properly, so I had to fork the repo. I have a pull request waiting but in the meantime, you can use my fork [here](https://github.com/samcrane8/Postdown).

## Testing

If you are working on the webapplication or a potential future mobile app, you may want to use the testing server such that you
do not have to run the business-logic server yourself.

That server can be found here: `devapi.icarusmap.com`.

Authentication is done via OAuth so you will need to generate custom values for `client_id` and `client_secret` to connect.
To do so, follow the tutorial found here in the django-oauth-toolkit documentation: [https://django-oauth-toolkit.readthedocs.io/en/latest/tutorial/tutorial_01.html](https://django-oauth-toolkit.readthedocs.io/en/latest/tutorial/tutorial_01.html).

## Partners

[Georgia Tech Police Department](http://www.police.gatech.edu/) was critical in the development of this system. The original IcarusMap project was with head of Physical Security, Jeffrey Hunnicutt, who met with our team weekly to hone this product to best help the campus.

## Contributors

### How to Help

If you would like to help, please send me an email (samcrane8@gmail.com) with the subject line starting with [FlyRight]. I also have not maintained a large open-sourced repository before so guidance on that front would be appreciated as well. Here are the things I would like to accomplish:

#### To Do

<ul>
  <li> Docker container setup scripts.
  <li> Unit Testing on the Front-End
  <li> Comprehensive unit-testing on the back-end server.
  <li> iOS app implementation.
  <li> airspace deconfliction
  <li> 3D flight plans
  <li> Setup watchdog to restart celery-worker if it ever crashes.
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

Sam Crane subsequently founded [Pelori](http://www.pelori.io) as a robotic solutions provider. Pelori provides deployment and server maintenance solutions, and is a major contributor to the FlyRight source code.
