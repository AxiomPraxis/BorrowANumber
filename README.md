# BorrowANumber

## Purpose

This was a project where I needed to solve an issue with multiple load performance tests simultaneously (using [k6](https://k6.io/)), the test users were experiencing collisions with usernames.

Rather than work out complex logic to have them determine which user number they were, I created this small development server to resolve it, all it does is serve up numbers for them. They borrow a number, and when they're done, they return it for another load test user.

Reminder this is just an example and no guarantees are provided. A Production grade WSGI server like gunicorn would be recommended over this basic flask example.

## Example Linux Installation

1. Install [Python](https://www.python.org/downloads/)
2. Install Redis Cluster (I used [redis-cluster helm chart from bitnami](https://bitnami.com/stack/redis-cluster/helm)) and [telepresence](https://www.telepresence.io/docs/latest/quick-start/?os=gnu-linux) on a [k3s cluster](https://k3s.io/), but regular redis-cluster works fine too.
3. (Optional) - setup virtualenv for your python
4. Install from requirements:
    `pip install -r requirements.txt`
5. Create a .env file with your variables:
    ```ini
    REDIS_PASSWORD="secret"
    RANGE_START=10000
    RANGE_AMOUNT=10000
    ```
    This example would serve numbers `10000-20000`
6. Run the server: `python BorrowANumber.py`


# REST API

The REST API to the example app is described below.

## Get list of checked numbers

### Request

`GET /checked`

    curl http://localhost:5000/checked

### Response headers

    Connection: close
    Content-Length: 27
    Content-Type: application/json
    Date: Fri, 01 Mar 2024 00:00:00 GMT
    Server: Werkzeug/3.0.1 Python/3.12.0

### Response body

```json
{
  "checked_out_numbers": []
}
```

## Check out a new number

### Request

`GET /check`

    curl http://localhost:5000/check

### Response headers

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 31
    Content-Type: application/json
    Date: Fri, 01 Mar 2024 00:00:00 GMT
    Server: Werkzeug/3.0.1 Python/3.12.0

### Response body

```json
{
    "checked_out_number": "16713"
}
```

## Return a number

### Request

`POST /return`

    curl -H "Content-Type: application/json" -XPOST http://localhost:5000/return

### Response headers

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 49
    Content-Type: application/json
    Date: Fri, 01 Mar 2024 00:00:00 GMT
    Server: Werkzeug/3.0.1 Python/3.12.0

### Response body

```json
{
  "message": "Number 16713 returned successfully"
}
```

## Reset all numbers

### Request

`GET /reset`

    curl http://localhost:5000/reset

### Response headers

    HTTP/1.1 200 OK
    Connection: close
    Content-Length: 17
    Content-Type: application/json
    Date: Fri, 01 Mar 2024 00:00:00 GMT
    Server: Werkzeug/3.0.1 Python/3.12.0

### Response body

```json
{
  "reset": "true"
}
```