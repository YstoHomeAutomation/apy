#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from rebel import Database, SqliteDriver
import json

class Device(object):
    def __init__(self, db):
        driver = SqliteDriver(db)
        self.db = Database(driver)

    def all(self):
        _dev = self.db.query('select * from Devices')
        return json.dumps({u'devices': list(_dev)})

    def get(self, id):
        _dev = self.db.query('select * from Devices where id = ?', id)
        return json.dumps({u'devices': list(_dev)})
        
    def new(self, id, description, switch_on, on_line, user_id):
        _dev = self.db.query('select * from Devices where id = ?', id)
        
        if _dev:
            raise ValueError
            
        _dev = self.db.execute("""
            insert into Devices(id, description, switch_on, on_line, created_at, updated_at, user_id)
            values(:id, :description, :switch_on, :on_line, (?), (?), :user_id)
        """, id, description, switch_on, on_line, datetime.now().strftime('%Y-%m%d %H:%M:%S'), datetime.now().strftime('%Y-%m%d %H:%M:%S'), user_id)
            
        return self.get(id)
        
    def update(self, id, description, switch_on, on_line):
        _dev = self.db.execute("""
            update Devices
            set description = :description,
                switch_on = :switch_on,
                on_line = :on_line,
                updated_at = (?)
            where id = :id
        """, description, switch_on, on_line, datetime.now().strftime('%Y-%m%d %H:%M:%S'), id)
        
        return self.get(id)
        
    def delete(self, id):
        _dev = self.db.query('select * from Devices where id = ?', id)
        if _dev:
            data = self.get(id)
            _dev = self.db.execute('delete from Devices where id = ?', id)
        else:
            raise ValueError
        
        return data
