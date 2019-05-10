# Icarus-Django

----------------



----------------

## Register Drone

```
POST {{url}}/drone/register_drone/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
>   "description" : "fixed-wing, 4\" blades",
>   "manufacturer" : "DJI",
>   "type": "quadrotor",
>   "color": "Green",
>   "name": "Droney!"
> }
> ```
> 

### Examples:

> 

----------------

## Edit Drone

```
POST {{url}}/drone/edit/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
>   "description" : "fixed-wing, 4\" blades",
>   "manufacturer" : "DJI",
>   "type": "quadrotor",
>   "color": "Green",
>   "name": "Droney!"
> }
> ```
> 

### Examples:

> 

----------------

## Get User Drones

```
GET {{url}}/drone/get_user_drones/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 

### Examples:

> 

----------------

## Delete Drone

```
POST {{url}}/drone/delete_drone/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> [
> 	{
>         "id": "8eaabfed-c7ad-4ed7-a371-a9b1a5b0ac78",
>         "name": "Droney!",
>         "owner_id": 1,
>         "description": "fixed-wing, 4\" blades",
>         "manufacturer": "DJI",
>         "type": "quadrotor",
>         "color": "Green",
>         "created_at": "2018-09-26T17:51:00.511296+00:00"
>     }
> ]
> ```
> 

### Examples:

> 

----------------

## Register Flight

```
POST {{url}}/mission/register/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
>   "title" : "tech",
>   "area": {
>         "type": "FeatureCollection",
>         "features": [
>             {
>             	"type": "Feature",
> 		        "properties": {},
>                 "geometry": {
>                     "coordinates":
>                     	[
>                         [
>                             33.78142341076552,
>                             -84.40747627542487
>                         ],
>                         [
>                             33.77814173337791,
>                             -84.40721878335944
>                         ],
>                         [
>                             33.77635816032391,
>                             -84.40575966165534
>                         ],
>                         [
>                             33.77500261996641,
>                             -84.4040430478858
>                         ],
>                         [
>                             33.773504366195404,
>                             -84.40159687326422
>                         ],
>                         [
>                             33.77296926921291,
>                             -84.39945110605231
>                         ],
>                         [
>                             33.77122126244645,
>                             -84.39893612192145
>                         ],
>                         [
>                             33.77129261035952,
>                             -84.3961895398902
>                         ],
>                         [
>                             33.77050778004809,
>                             -84.39593204782477
>                         ],
>                         [
>                             33.76968726794511,
>                             -84.392370074253
>                         ],
>                         [
>                             33.768866747984966,
>                             -84.39194092081061
>                         ],
>                         [
>                             33.76890242292924,
>                             -84.39061054513922
>                         ],
>                         [
>                             33.77122126244645,
>                             -84.39061054513922
>                         ],
>                         [
>                             33.77400378703043,
>                             -84.39052471445075
>                         ],
>                         [
>                             33.77664353450811,
>                             -84.39121135995856
>                         ],
>                         [
>                             33.78028197202204,
>                             -84.39129719064704
>                         ],
>                         [
>                             33.7814947501819,
>                             -84.3915975980567
>                         ],
>                         [
>                             33.78142341076552,
>                             -84.40747627542487
>                         ]
>                     ],
>                     "type": "Polygon"
>                 }
>             }
>         ]
>     },
>   "description" : "testing minimap",
>   "starts_at": "2018-11-12T11:45:00+05",
>   "ends_at": "2018-11-12T12:45:00+05",
>   "type": "commercial"
> }
> ```
> 

### Examples:

> 

----------------

## Add Drone

```
POST {{url}}/flight/add_drone/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> { 
> 	"drone_id": "89b11d21-5c6c-44dc-aa32-f54bb0f924ac",
> 	"mission_id": "f602a0b3-c552-4b5b-929d-c440dea8097b"
> }
> ```
> 

### Examples:

> 

----------------

## Remove Drone

```
POST {{url}}/flight/remove_drone/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> { 
> 	"drone_id": "5b309275-8f3f-484b-8e74-ac9e3e47f25b",
> 	"mission_id": "7b2067f6-81e9-49a2-9672-c818d31614b8"
> }
> ```
> 

### Examples:

> 

----------------

## Edit Flight

```
POST {{url}}/mission/edit/
```

Allows user to edit the details of a mission.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
>   "mission_id" : "fc6c59d4-c57e-4c39-9e6a-c2c493df7c82",
>   "title": "South Georgia",
>   "description": "Looking for someone in South Georgia",
>   "area": {
>         "type": "FeatureCollection",
>         "features": [
>             {
>                 "geometry": {
>                     "coordinates": [
>                         [
>                             -78.046875,
>                             13.581920900545844
>                         ],
>                         [
>                             -73.47656249999999,
>                             -3.162455530237848
>                         ],
>                         [
>                             -60.8203125,
>                             14.26438308756265
>                         ],
>                         [
>                             -78.046875,
>                             13.581920900545844
>                         ]
>                     ],
>                     "type": "Polygon"
>                 }
>             }
>         ]
>     }
> }
> ```
> 

### Examples:

> 

----------------

## Delete Flight

```
POST {{url}}/flight/delete/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"mission_id": "abdf5ed9-b2ed-4db1-8b75-3fe997d2ea7b"
> }
> ```
> 

### Examples:

> 

----------------

## Get Flights

```
GET {{url}}/flight/get/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 

### Examples:

> 

----------------

## Get Flights

```
POST {{url}}/flight/get/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"filters": [
> 		{
> 			"title": "before",
> 			"datetime": "2017-12-11T10:19:00+00"
> 		},
> 		{
> 			"title": "after",
> 			"datetime": "2016-09-11T10:19:00+00"
> 		}
> 	]
> }
> ```
> 

### Examples:

> 

----------------

## Get Between

```
GET {{url}}/flight/get_between/?starts_at=2016-12-11T10%3A19%3A00%2B00&ends_at=2018-12-11T10%3A19%3A00%2B00
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |starts_at|2016-12-11T10%3A19%3A00%2B00||
> |ends_at|2018-12-11T10%3A19%3A00%2B00||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"starts_at": "2017-12-11T10:19:00+00",
> 	"ends_at": "2017-12-11T10:19:00+00"
> }
> ```
> 

### Examples:

> 

----------------

## Get Mission Info

```
POST {{url}}/flight/get_info/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"mission_id": "fc6c59d4-c57e-4c39-9e6a-c2c493df7c82"
> }
> ```
> 

### Examples:

> 

----------------

## Edit Flight Clearance

```
POST {{url}}/flight/edit_clearance/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"mission_id": "fc6c59d4-c57e-4c39-9e6a-c2c493df7c82",
> 	"state": "NOTIFICATION RECEIVED",
> 	"message": "This looks good."
> }
> ```
> 

### Examples:

> 

----------------

## Get Drones

```
POST {{url}}/flight/get_drones/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"mission_id": "502ea105-196e-4c66-b26c-f9ab3d8465ac"
> }
> ```
> 

### Examples:

> 

----------------

## Get Past Missions

```
GET {{url}}/flight/get_past/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 

### Examples:

> 

----------------

## Get Upcoming Missions

```
GET {{url}}/flight/get_upcoming/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 

### Examples:

> 

----------------

## Login

```
POST {{url}}/o/token/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/x-www-form-urlencoded||
> 
> **Body**
> 
> |Key|Value|Type|Description|
> |---|---|---|---|
> |grant_type|password|text||
> |client_id|{{client_id}}|text||
> |client_secret|{{client_secret}}|text||
> |username|admin|text||
> |password|lawrence71|text||
> 

### Examples:

> 

----------------

## Register User

```
POST {{url}}/user/register_user/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"username": "samcrane8",
> 	"password": "lawrence8",
> 	"email": "samcrane8@gmail.com"
> }
> ```
> 

### Examples:

> 

----------------

## Change Password

```
POST {{url}}/user/change_password/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"old_password": "lawrence",
> 	"new_password": "maddy"
> }
> ```
> 

### Examples:

> 

----------------

## Update User Info

```
POST {{url}}/user/update/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"username": "samcrane6",
> 	"password": "lawrence6",
> 	"email": "samcrane8@gmail.com",
> 	"picture_url": "guy.jpg"
> }
> ```
> 

### Examples:

> 

----------------

## Logout

```
POST {{url}}/o/revoke_token/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/x-www-form-urlencoded||
> 
> **Body**
> 
> |Key|Value|Type|Description|
> |---|---|---|---|
> |token|{{access_token}}|text||
> |client_id|{{client_id}}|text||
> |client_secret|{{client_secret}}|text||
> 

### Examples:

> 

----------------

## Get User

```
GET {{url}}/user/get/?id=39
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |id|39||
> 

### Examples:

> 

----------------

## Get Current User

```
GET {{url}}/user/get_current/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

## Is User Logged In

```
GET {{url}}/user/is_logged_in/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

## Forgot Password

```
GET {{url}}/user/forgot_password/?email=samcrane8@gmail.com
```

Endpoint to request an email to reset your password.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |email|samcrane8@gmail.com||
> 

### Examples:

> 

----------------

## Update Pilot Info

```
POST {{url}}/pilot/update/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"faa_registration_number": "123",
> 	"remote_pilot_certificate_number": "456",
> 	"mobile_phone_number": "samcrane8@gmail.com"
> }
> ```
> 

### Examples:

> 

----------------

## Register Pilot

```
POST {{url}}/pilot/register/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
>{ 
>	"username": "anushk_test",
>	"password": "anushk_test",
>	"email": "anushk_test@gmail.com",
>	"mobile_phone_number": "4247718471",
>	"remote_pilot_certificate_number": "456",
>	"first_name": "anushk_test",
>	"last_name": ""
>}
> ```
> 

### Examples:

> 

----------------

## Get Pilot

```
GET {{url}}/pilot/get/?id=61
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |id|61||
> 

### Examples:

> 

----------------

## Is Government Official

```
GET {{url}}/department/is_government_official/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

## Get Departments

```
GET {{url}}/department/get/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

## Get Department Info

```
GET {{url}}/department/get/?id=
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |id|||
> 

### Examples:

> 

----------------

## Get User Departments

```
GET {{url}}/department/get/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

## Info

```
GET {{url}}/department/info/?id=4
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |id|4||
> 

### Examples:

> 

----------------

## Add Airboss

```
POST {{url}}/department/add_airboss/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"name": "Georgia Tech Police Department", 
> 	"airboss_id": 30
> }
> ```
> 

### Examples:

> 

----------------

## Remove Airboss

```
POST {{url}}/department/remove_airboss/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"name": "Hawaii University Police Department", 
> 	"airboss_id": 1
> }
> ```
> 

### Examples:

> 

----------------

## Add Watch Commander

```
POST {{url}}/department/add_watch_commander/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"name": "Georgia Tech Police Department", 
> 	"watch_commander_id": 1
> }
> ```
> 

### Examples:

> 

----------------

## Remove Watch Commander

```
POST {{url}}/department/remove_watch_commander/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"name": "Georgia Tech Police Department", 
> 	"watch_commander_id": 61
> }
> ```
> 

### Examples:

> 

----------------

## Create Department

```
POST {{url}}/department/create/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"name": "Georgia Tech Police Department",
> 	"owner_id": 1,
> 	"area": {
>         "type": "FeatureCollection",
>         "features": [
>             {
>             	"type": "Feature",
>             	"properties": {},
>                 "geometry": {
>                     "coordinates": [
>                         [
>                             33.78142341076552,
>                             -84.40747627542487
>                         ],
>                         [
>                             33.77814173337791,
>                             -84.40721878335944
>                         ],
>                         [
>                             33.77635816032391,
>                             -84.40575966165534
>                         ],
>                         [
>                             33.77500261996641,
>                             -84.4040430478858
>                         ],
>                         [
>                             33.773504366195404,
>                             -84.40159687326422
>                         ],
>                         [
>                             33.77296926921291,
>                             -84.39945110605231
>                         ],
>                         [
>                             33.77122126244645,
>                             -84.39893612192145
>                         ],
>                         [
>                             33.77129261035952,
>                             -84.3961895398902
>                         ],
>                         [
>                             33.77050778004809,
>                             -84.39593204782477
>                         ],
>                         [
>                             33.76968726794511,
>                             -84.392370074253
>                         ],
>                         [
>                             33.768866747984966,
>                             -84.39194092081061
>                         ],
>                         [
>                             33.76890242292924,
>                             -84.39061054513922
>                         ],
>                         [
>                             33.77122126244645,
>                             -84.39061054513922
>                         ],
>                         [
>                             33.77400378703043,
>                             -84.39052471445075
>                         ],
>                         [
>                             33.77664353450811,
>                             -84.39121135995856
>                         ],
>                         [
>                             33.78028197202204,
>                             -84.39129719064704
>                         ],
>                         [
>                             33.7814947501819,
>                             -84.3915975980567
>                         ],
>                         [
>                             33.78142341076552,
>                             -84.40747627542487
>                         ]
>                     ],
>                     "type": "Polygon"
>                 }
>             }
>         ]
>     }
> }
> ```
> 

### Examples:

> 

----------------

## Flight Histogram

```
POST {{url}}/department/flight_histogram/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"department_id": 4,
> 	"start_day": "2018-10-21T00:00:00+00",
> 	"end_day": "2018-10-21T00:00:00+00"
> }
> ```
> 

### Examples:

> 

----------------

## Message Jurisdiction

```
POST {{url}}/official/message_jurisdiction/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
> 	"department_name": "department_name",
> 	"message": "hello!"
> }
> ```
> 

### Examples:

> 

----------------

## Add Airspace Restriction

```
POST {{url}}/airspace/add_airspace_restriction/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 
> **Header**
> 
> |Key|Value|Description|
> |---|---|---|
> |Content-Type|application/json||
> 
> **Body**
> 
> ```
> {
>   "title" : "Venezuela",
>   "area" : {
>     "type": "FeatureCollection",
>     "features": [
>       {
>         "type": "Feature",
>         "geometry": {
>           "type": "Polygon",
>           "coordinates": 
>             [
>               [
>                 -78.046875,
>                 13.581920900545844
>               ],
>               [
>                 -73.47656249999999,
>                 -3.162455530237848
>               ],
>               [
>                 -60.8203125,
>                 14.26438308756265
>               ],
>               [
>                 -78.046875,
>                 13.581920900545844
>               ]
>             ]
>         },
>         "properties": {}
>       }
>     ]
>   },
>   "is_constant": false,
>   "description" : "testing minimap",
>   "starts_at": "2011-10-12T11:45:00+05",
>   "ends_at": "2011-11-12T11:45:00+05",
>   "type": "Class-C"
> }
> ```
> 

### Examples:

> 

----------------

## Get Unread Notifications

```
GET {{url}}/user/get/?id=39
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |id|39||
> 

### Examples:

> 

----------------

## Feed

```
GET {{url}}/notification/feed/?count=5
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |count|5||
> 

### Examples:

> 

----------------

## Read

```
GET {{url}}/notification/read/?id=64
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> |id|64||
> 

### Examples:

> 

----------------

## Read All

```
GET {{url}}/notification/read_all/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

## Unread Count

```
GET {{url}}/inbox/notifications/api/unread_count/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

## Unread List

```
GET {{url}}/inbox/notifications/api/unread_list/
```



----------------

### Request

> 
> **Query**
> 
> |Key|Value|Description|
> |---|---|---|
> ||||
> 

### Examples:

> 

----------------

----------------

Built with [Postdown][PyPI].

Author: [Titor](https://github.com/TitorX)

[PyPI]:    https://pypi.python.org/pypi/Postdown
