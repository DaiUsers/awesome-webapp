#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from models import User, Comment, Blog, next_id

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@([a-z0-9\-\_]+[a-z0-9\.\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

@get('/')
async def index(request):
	summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
	blogs = [
		Blog(id='1',name='Test Blog', summary=summary, created_at=time.time()-120),
		Blog(id='2',name='Something New', summary=summary, created_at=time.time()-3600),
		Blog(id='3',name='Learn Swift', summary=summary, created_at=time.time()-7200),
		Blog(id='4',name='Learn Java', summary=summary, created_at=time.time()-10200),
		Blog(id='5',name='Learn Python', summary=summary, created_at=time.time()-10600),
		Blog(id='6',name='Learn HTML5', summary=summary, created_at=time.time()-15200),
	]
	#users = await User.findAll()
	return {
		'__template__': 'blogs.html',
		'blogs': blogs
	}



@post('/api/users')
def api_register_user(*, email, name, passwd):
	if not name or not name.strip():
		raise APIValueError('name')
	if not email or not _RE_EMAIL.match(email):
		raise APIValueError('email')
	if not passwd or not _RE_SHA1.match(passwd):
		raise APIValueError('passwd')
	users = yield from User.findAll('email=?', [email])
	if len(users) > 0:
		raise APIError('register:failed', 'email', 'Email is already in use.')
	uid = next_id()
	sha1_passwd = '%s:%s' % (uid, passwd)
	user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
	yield from user.save()
	
	r = web.Response()
	r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
	user.passwd = '******'
	r.content_type = 'application/json'
	r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
	return r
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
