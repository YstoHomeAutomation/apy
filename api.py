#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import request, response
from bottle import get, post, delete, run, HTTPError
from bottle_rest import json_to_params

from model import device

dev = device.Device('ysto.db')

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
def create_device(id, description, swith_on, on_line, user_id):
    try:
        data = dev.new(id, description, swith_on, on_line, user_id)
    except:
        raise HTTPError(400, "'somevar' parameter is required!")
    
    return data
    
@post('/devices/<id>')
@json_to_params
def update_device(id, description, swith_on, on_line):
    return dev.update(id, description, swith_on, on_line)
    
@delete('/devices/<id>')
def delete(id):
    return dev.delete(id)

@get('/users')
def users():
    return {'users': 'Lista de usuarios'}


if __name__ == '__main__':
    run(host='0.0.0.0', port=3001, debug=True)
