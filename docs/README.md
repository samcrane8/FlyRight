# Icarus-Django

----------------



----------------

## Drone

```
POST {{url}}/drone/delete_drone/
```

### Request

> 
> **Query**
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

## Flight

```
GET {{url}}/flight/get_upcoming/
```

### Request

> 
> **Query**
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

## User

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

## Pilot

```
GET {{url}}/pilot/get/?id=61
```

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

## Department

```
POST {{url}}/official/message_jurisdiction/
```

Upgrade the given user to a government official. Only to be done by admin users.

----------------

### Request

> 
> **Query**
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

## Airspace Restriction

```
POST {{url}}/airspace/add_airspace_restriction/
```

### Request

> 
> **Query**
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

## Notifications

```
GET {{url}}/inbox/notifications/api/unread_list/
```

### Request

> 
> **Query**
> 

### Examples:

> 

----------------

----------------

Built with [Postdown][PyPI].

Author: [Titor](https://github.com/TitorX)

[PyPI]:    https://pypi.python.org/pypi/Postdown
