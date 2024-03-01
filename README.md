# BorrowANumber

## Purpose

This was a project where I needed to solve an issue with multiple load performance tests simultaneously (using [k6](https://k6.io/)), the test users were experiencing collisions with usernames.

Rather than work out complex logic to have them determine which user number they were, I created this small development server to resolve it, all it does is serve up numbers for them. They borrow a number, and when they're done, they return it for another load test user.

Reminder this is just an example and no guarantees are provided.

## Example Linux Installation

1. Install Python (up to 3.12)
2. Install Redis Cluster (I used [redis-cluster helm chart from bitnami](https://bitnami.com/stack/redis-cluster/helm)) and [telepresence](https://www.telepresence.io/docs/latest/quick-start/?os=gnu-linux) on a [k3s cluster](https://k3s.io/), but regular redis-cluster works fine too.
3. (Optional) - setup virtualenv for your python
4. Install from requirements:
    `pip install -r requirements.txt`
5. Create a .env file with your REDIS_PASSWORD variable:
    `echo REDIS_PASSWORD=secret > .env`
6. Run the server: `python BorrowANumber.py`

## Usage

### HTTP REST API methods

1. /reset (GET) - wipe all checked out and checkable numbers
2. /check (GET) - check a number out
3. /checked (GET) - see all checked out numbers
4. /return (POST) - return a checked out number.

### Example /return POST Syntax:

with header "Content-Type: application/json"
```json
{
    "number": 10000    
}
```
