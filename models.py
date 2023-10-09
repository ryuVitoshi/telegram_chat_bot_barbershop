import sqlite3
import credentials

class User:
    def __init__(self, name):
        self.name = name
        self.phone = None

class Service:
    def __init__(self, name):
        self.name = name
        self.info = None
        self.price = None

class Employee:
    def __init__(self, name):
        self.name = name
        self.role = None
        self.phone = None

class Schedule:
    def __init__(self, name):
        self.name = name
        self.date = None
        self.start_time = None
        self.shift_time = None

class Appointment:
    def __init__(self, user):
        self.user = user
        self.service = None
        self.service_name = None
        self.comments = None
        self.app_date = None
        self.app_time = None
        self.app_id = None

user_dict = {}
employee_dict = {}
schedule_dict = {}
services_list = []
apps_dict = {}
state = {}
