import redis, random
# # Function to initialize the database connection


def initialize_redis_connection():
    r = redis.Redis(host='0.0.0.0', port=6379, db=0)
    return r


# Function add user
def add_response_into_db(connection , id_, code_output):
    connection.set(id_,code_output)

