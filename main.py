from threads.redis_thread import RedisClientThread
from threads.sql_thread import SQLClientThread

if __name__ == '__main__':
    sql_client = SQLClientThread(currency_pair='BTCUSDT', interval=5)
    redis_client = RedisClientThread(currency_pair='LTCUSDT', interval=8)

    sql_client.start()
    redis_client.start()

    sql_client.join()
    redis_client.join()
