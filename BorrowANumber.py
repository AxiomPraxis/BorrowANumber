import os
from flask import Flask, jsonify, request
import random
from redis.cluster import RedisCluster
import dotenv

dotenv.load_dotenv()

REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
RANGE_START = int(os.environ["RANGE_START"])
RANGE_AMOUNT = int(os.environ["RANGE_AMOUNT"])
RANGE_END = RANGE_START + RANGE_AMOUNT

redis_db = RedisCluster(host="redis-cluster.infra.svc.cluster.local", port=6379, password=REDIS_PASSWORD)

app = Flask(__name__)
checkable_numbers = set()
checked_out_numbers = set()

@app.route('/check', methods=['GET'])
def check_number():
	checkable_numbers = redis_db.smembers('checkable_numbers')
	
	if not checkable_numbers:
		return jsonify({'message': 'No numbers available to check out'})
	
	number_to_check_out = random.choice(list(checkable_numbers))
	
	redis_db.srem('checkable_numbers', number_to_check_out)
	redis_db.sadd('checked_out_numbers', number_to_check_out)
	
	return jsonify({'checked_out_number': number_to_check_out.decode('utf-8')})

  

@app.route('/return', methods=['POST'])
def return_number():

	data = request.get_json()
	if type(data.get('number')) == int:
		number = str(data.get('number'))
	else:
		number = data.get('number')
	checked_out_numbers = redis_db.smembers('checked_out_numbers')
	
	int_set = {(bytes_value.decode('utf-8')) for bytes_value in checked_out_numbers}

	if number is None:
		return jsonify({'error': 'Please provide a valid number to return'}), 400
	
	if number not in int_set:
		return jsonify({'error': 'Please provide a valid number to return'}), 400
	
	redis_db.srem('checked_out_numbers', number)
	redis_db.sadd('checkable_numbers', number)
	
	return jsonify({'message': f'Number {number} returned successfully'})

  

@app.route('/checked', methods=['GET'])
def get_checked_numbers():
	checked_out_numbers = redis_db.smembers('checked_out_numbers')

	return jsonify({'checked_out_numbers': [num.decode('utf-8') for num in checked_out_numbers]})

@app.route('/reset', methods=['GET'])
def reset_numbers():
	num_list = range(RANGE_START,RANGE_END)
	
	for x in num_list:
		redis_db.sadd('checkable_numbers', x)

	checked_out_numbers = redis_db.smembers('checked_out_numbers')
	int_set = {(bytes_value.decode('utf-8')) for bytes_value in checked_out_numbers}
	
	if int_set:
		for x in int_set:
			redis_db.srem('checked_out_numbers', x)
	
	return jsonify({"reset": "true"})

  

if __name__ == '__main__':
	app.run(debug=False, port=5000, host='0.0.0.0')