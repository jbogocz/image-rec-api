
# Image Recognition RESTful API
REST API using Tensorflow, Flask, Docker, MongoDB

## Usage
To build docker image:
```
docker-compose build
```
Run api:
```
docker-compose up
```
#### Sending POST requests to:
1\. localhost:5000/register <br />

```json
{
  "username": "your_username",
  "password": "your_password"
}
```
Response:
```json
{
  "msg": "You successfully signed up for this API",
  "status": 200
}
```
2\. localhost:5000/classify <br />

```json
{
  "username": "your_username",
  "password": "your_password",
  "url": "zebra_image_url.jpg"
}
```
Response:
```json
{
  "zebra": 0.984,
  "hartebeest": 0.002,
  "tiger": 0.001,
}
```
3\.  localhost:5000/refill <br />

```json
{
  "username": "your_username",
  "admin_pw": "admin1",
  "amount": "token_amount"
}
```
Response:
```json
{
  "msg": "Refilled",
  "status": 200
}
```
