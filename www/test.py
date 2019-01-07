
import orm
from Model import User, Blog, Comment
import asyncio

def test():
    yield from orm.create_pool(loop=None,user='root', password='', database='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    yield from u.save()

for x in test():
    pass
