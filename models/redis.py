import redis
import random
import hashlib

def add_in_queue(user_id):
    with redis.Redis() as r:
        r.rpush('search_queue', user_id)
def del_from_queue(user):
    with redis.Redis() as r:
        r.lrem("search_queue",0,user)
def get_interlocutor(user):
    with redis.Redis() as r:
        if r.llen("search_queue") >= 2:
            r.lrem("search_queue",0,user)
            return int(r.lpop("search_queue").decode("utf-8"))
        else:
            return False
def check_queue():
    with redis.Redis() as r:
        if r.llen("search_queue") >= 2:
            return True
        else:
            return False       
def create_dialogue(user_1,user_2):
    with redis.Redis() as r:
        # value = f"{user_1}{user_2}".encode()
        # hash = hashlib.sha256(value).hexdigest()
        r.hset(f"dialogues",user_1,user_2)
        r.hset(f"dialogues",user_2,user_1)
        # r.hset(f"states", user_1,"chating")
        # r.hset(f"states", user_2,"chating")
def del_dialogue(user1,user2):
    with redis.Redis() as r:
        r.hdel("dialogues", user1)
        r.hdel("dialogues", user2)
def find_dialogue(id):
    with redis.Redis() as r:
        return int(r.hget("dialogues", id).decode("utf-8"))
def check(user) -> bool:
    with redis.Redis() as r:
        if r.hget("states", user):
            return True
        else:
            return False

