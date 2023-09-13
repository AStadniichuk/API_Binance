from api_clients.redis_client import RedisClient
from api_clients.sql_client import SQLClient

if __name__ == '__main__':
    sql_client = SQLClient(currency_pair='BTCUSDT', interval=5, max_iterations=10)
    redis_client = RedisClient(currency_pair='LTCUSDT', interval=8, max_iterations=10)

    sql_client.start()
    redis_client.start()

    sql_client.join()
    redis_client.join()
