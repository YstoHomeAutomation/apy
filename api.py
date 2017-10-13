#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import get, post, delete, run

@get('/')
def about():
    return {'about': 'ysto-API', 'versao': '2.0.0'}

@get('/devices')
def devices():
    return {'devices': 'lista de dispositivos'}

@get('/users')
def users():
    return {'users': 'Lista de usuarios'}


if __name__ == '__main__':
    run(host='0.0.0.0', port=3001, debug=True)
