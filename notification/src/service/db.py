import redis, time
# # Function to initialize the database connection


def initialize_redis_connection():
    r = redis.Redis(host='0.0.0.0', port=6379, db=0)
    return r


# Function add user
def get_response_from_db(connection , id_):
    time.sleep(0.1)
    s_time = time.time()
    while not connection.get(id_):
        time.sleep(0.5)
        pass
    code_output_bytes = connection.get(id_)
    code_output = code_output_bytes.decode('utf-8')
    connection.delete(id_)
    return code_output

