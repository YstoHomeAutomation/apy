#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request, response, install, HTTPError
from bottle import get, post, delete, put, run
from bottle_rest import json_to_params
from bottlejwt import JwtPlugin

from model import device
from model import user

dev = device.Device('ysto.db')
u = user.User('ysto.db')

install(JwtPlugin(u.validation, 'secret', algorithm='HS256'))

@get('/')
def about():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return {'about': 'ysto-API', 'versao': '2.0.0'}

@get('/devices', auth=1)
def devices():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.all()
    
@get('/devices/<id>', auth=1)
def devices(id):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.get(id)
    
@post('/devices', auth=1)
@json_to_params
def create_device(id, description, switch_on, on_line, user_id):
    try:
        data = dev.new(id, description, switch_on, on_line, user_id)
    except:
        raise HTTPError(400, "'somevar' parameter is required!")
    
    return data
    
@post('/devices/<id>', auth=1)
@json_to_params
def update_device(id, description, switch_on, on_line):
    return dev.update(id, description, switch_on, on_line)
    
@put('/devices/<id>', auth=1)
@json_to_params
def device_switch(id, switch_on):
    return dev.turn_on(id, switch_on)

    
@delete('/devices/<id>', auth=1)
def delete_device(id):
    return dev.delete(id)

@get('/users', auth=1)
def users():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    return u.all()
    
@get('/users/<id>', auth=1)
def users(id):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return u.get(id)

@post('/users', auth=1)
@json_to_params
def create_user(id, name, password, email):
    try:
        data = u.new(id, name, password, email)
    except:
        raise HTTPError(400, "SOMEVAR parameter is required!")
    
    return data
    
@post('/users/<id>', auth=1)
@json_to_params
def update_user(id, name, password, email):
    return u.update(id, name, password, email)
    
@delete('/users/<id>', auth=1)
def delete_user(id):
    return u.delete(id)
    
@post('/auth')
@json_to_params
def login(email, password):
    id = u.login(email, password)
    if id:
        return JwtPlugin.encode({'id': id})
    else:
        raise HTTPError(401)



if __name__ == '__main__':
    run(host='0.0.0.0', port=3001, debug=True)
