#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request, response
from bottle import get, post, delete, put, run
from bottle_rest import json_to_params

from model import device
from model import user

dev = device.Device('ysto.db')
u = user.User('ysto.db')

@get('/')
def about():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return {'about': 'ysto-API', 'versao': '2.0.0'}

@get('/devices')
def devices():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.all()
    
@get('/devices/<id>')
def devices(id):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return dev.get(id)
    
@post('/devices')
@json_to_params
def create_device(id, description, switch_on, on_line, user_id):
    try:
        data = dev.new(id, description, switch_on, on_line, user_id)
    except:
        raise HTTPError(400, "'somevar' parameter is required!")
    
    return data
    
@post('/devices/<id>')
@json_to_params
def update_device(id, description, switch_on, on_line):
    return dev.update(id, description, switch_on, on_line)
    
@put('/devices/<id>')
@json_to_params
def device_switch(id, switch_on):
    return dev.turn_on(id, switch_on)

    
@delete('/devices/<id>')
def delete_device(id):
    return dev.delete(id)

@get('/users')
def users():
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    
    return u.all()
    
@get('/users/<id>')
def users(id):
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'

    return u.get(id)

@post('/users')
@json_to_params
def create_user(id, name, password, email):
    try:
        data = u.new(id, name, password, email)
    except:
        raise HTTPError(400, "SOMEVAR parameter is required!")
    
    return data
    
@post('/users/<id>')
@json_to_params
def update_user(id, name, password, email):
    return u.update(id, name, password, email)
    
@delete('/users/<id>')
def delete_user(id):
    return u.delete(id)


if __name__ == '__main__':
    run(host='0.0.0.0', port=3001, debug=True)
