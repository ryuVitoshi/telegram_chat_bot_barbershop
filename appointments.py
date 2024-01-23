from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import credentials
import design
import sqlite3
import texts
import services
import registration
import menu
from datetime import datetime, timedelta
import random

from credentials import bot
from credentials import database

employees = []
employees_list = []

# Converts time format "00:00" to amount of minutes passed since midnight
def time_to_minutes(time):
    return int(time[:2])*60+int(time[3:5])

# Converts amount of minutes passed since midnight to time format "00:00"
def minutes_to_time(minutes):
    return str(minutes//60).zfill(2) + ":" + str(minutes%60).zfill(2)

# Function to update list of employees
def update_employees():
    con = sqlite3.connect(database)
    c = con.cursor()
    c.execute('SELECT * FROM employees')
    data = c.fetchall()
    con.close()
    if data is None:
        return None
    global employees
    global employees_list
    for element in data:
        info = {
        'id': element[0],
        'full_name': element[1],
        'role': element[2],
        'phone': element[3]
        }
        employees.append(info)
        employees_list.append(info['full_name'])
update_employees()

# Function to get info about employee by attribute
def get_employee(input_attr, value, output_attr=None):
    global employees
    for empl in employees:
        if empl[input_attr] == value:
            if output_attr is None:
                return empl
            return empl[output_attr]
    return None

# Function to get available dates for scheduling
def get_available_date(service, employee_name, ignore_app_id=None):
    output = []
    for i in range(1, 8):
        date = (datetime.now().date()+timedelta(days=i)).strftime("%d.%m.%Y")
        if get_available_time(service, date, employee_name, ignore_app_id):
            output.append(date)
    return output

#
def get_available_employees(service, date, ignore_app_id=None):
    service_time = int(services.get_service('name', service, 'time'))
    output = list()
    global employees_list
    empls = employees_list
    con = sqlite3.connect(database)
    c = con.cursor()
    for empl in empls:
        c.execute('SELECT app_time, service, app_id FROM appointments WHERE app_date=? AND employee=?',
                  (date, get_employee('full_name', empl, 'id'),))
        data = c.fetchall()
        time_start = time_to_minutes('10:00')
        time_end = time_to_minutes('16:00')-service_time
        times = list(range(time_start, time_end+20, 20))
        for item in data:
            if item[2] == ignore_app_id:
                continue
            left = time_to_minutes(item[0])-service_time
            right = time_to_minutes(item[0])+int(services.get_service('id', item[1], 'time'))
            times = list(filter(lambda x: x <= left or x >= right, times))
        if times:
            output.append(empl)
    con.close()
    return output

# Function to get available times for a specific date and employee (if given)
def get_available_time(service, date, employee_name, ignore_app_id=None):
    service_time = int(services.get_service('name', service, 'time'))
    output = set()
    global employees_list
    empls = employees_list
    if employee_name is not None and employee_name != "Any employee":
        empls = [employee_name]
    con = sqlite3.connect(database)
    c = con.cursor()
    for empl in empls:
        c.execute('SELECT app_time, service, app_id FROM appointments WHERE app_date=? AND employee=?',
                  (date, get_employee('full_name', empl, 'id'),))
        data = c.fetchall()
        time_start = time_to_minutes('10:00')
        time_end = time_to_minutes('16:00')-service_time
        times = list(range(time_start, time_end+20, 20))
        for item in data:
            if item[2] == ignore_app_id:
                continue
            left = time_to_minutes(item[0])-service_time
            right = time_to_minutes(item[0])+int(services.get_service('id', item[1], 'time'))
            times = list(filter(lambda x: x <= left or x >= right, times))
        output.update(times)
    con.close()
    return [minutes_to_time(time) for time in sorted(list(output))]

# Get user appointments
def get_appointments(user_id):
    con = sqlite3.connect(credentials.database)
    c = con.cursor()
    c.execute('SELECT * FROM appointments WHERE user=?',(user_id,))
    data = c.fetchall()
    con.close()
    if data is None:
        return None
    appointments = []
    for element in data:
        info = {
        'id': element[0],
        'date': element[1],
        'time': element[2],
        'comments': element[3],
        'user': element[4],
        'service': element[5],
        'employee': element[6]
        }
        appointments.append(info)
    return appointments

def sign_up(user_id, service, date, employee, time, ignore_app_id=None):
    if employee == "Any employee":
        empls = [empl for empl in get_available_employees(service, date) if time in get_available_time(service, date, empl, ignore_app_id)]
        if not empls:
            return False
        employee = random.choice(empls)
    con = sqlite3.connect(database)
    c = con.cursor()
    c.execute('INSERT INTO appointments (app_date, app_time, user, service, employee) VALUES (?, ?, ?, ?, ?)',
              (date, time, user_id, services.get_service('name', service, 'id'), get_employee('full_name', employee, 'id')))
    con.commit()
    con.close()
    return True

#
def delete_appointment(app_id):
    con = sqlite3.connect(database)
    c = con.cursor()
    c.execute('DELETE FROM appointments WHERE app_id=?', (app_id,))
    con.commit()
    con.close()

# ------Menu------

# Send user their appointments
def send_appointments(message):
    user_id = message.from_user.id
    apps = ["➕ Sign up for an appointment"]
    apps.extend([app['date'][:5]+', '+app['time']+', '+services.get_service('id', app['service'], 'name')+', '+get_employee('id', app['employee'], 'full_name') for app in get_appointments(user_id)])
    bot.send_message(user_id, texts.SIGN_UP, parse_mode='html', reply_markup=design.keyboard(apps, n_cols=1))
    bot.register_next_step_handler(message, process_appointments_selection)

#
def process_appointments_selection(message):
    user_id = message.from_user.id
    choice = message.text
    appointments = get_appointments(user_id)
    apps = [app['date'][:5]+', '+app['time']+', '+services.get_service('id', app['service'], 'name')+', '+get_employee('id', app['employee'], 'full_name') for app in appointments]
    if choice == "➕ Sign up for an appointment":
        data = registration.get_user_data(user_id)
        if data is not None:
            sign_up_service(message)
        else:
            text = "You are not registered. Let's get you registered!\nPlease share your phone number:"
            bot.send_message(user_id, text, reply_markup=design.keyboard(['Share your phone']))
            bot.register_next_step_handler(message, registration.process_phone_number)
    elif choice in apps:
        app = appointments[apps.index(choice)]
        change_appointment(message, app)
    elif choice == design.menu_navigation[0]:
        menu.send_welcome(message)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_appointments_selection)

# Sign up message
def sign_up_service(message):
    user_id = message.from_user.id
    bot.send_message(user_id, texts.SIGN_UP, parse_mode='html', reply_markup = design.keyboard(services.services_list, n_cols=2))
    bot.register_next_step_handler(message, process_sign_up_service)

#
def process_sign_up_service(message):
    user_id = message.from_user.id
    choice = message.text
    if choice in services.services_list:
        sign_up_date(message, choice)
    elif choice == design.menu_navigation[0]:
        send_appointments(message)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_appointments_selection)

# Choose date to sign up
def sign_up_date(message, service):
    user_id = message.from_user.id
    text = message.text
    dates = get_available_date(service, None)
    text = "Choose date below:"
    bot.send_message(user_id, text, parse_mode='html', reply_markup = design.keyboard(dates, n_cols=2))
    bot.register_next_step_handler(message, process_sign_up_date, service, dates)

#
def process_sign_up_date(message, service, dates):
    user_id = message.from_user.id
    choice = message.text
    if choice in dates:
        sign_up_employee(message, service, choice)
    elif choice == design.menu_navigation[0]:
        sign_up_service(message)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_sign_up_date, service, dates)

# Choose employee to sign up
def sign_up_employee(message, service, date):
    user_id = message.from_user.id
    text = message.text
    empls = ['Any employee']
    empls.extend(get_available_employees(service, date))
    if len(empls) == 1:
        empls.clear()
    text = "Choose employee below:"
    bot.send_message(user_id, text, parse_mode='html', reply_markup = design.keyboard(empls, n_cols=2))
    bot.register_next_step_handler(message, process_sign_up_employee, service, date, empls)

#
def process_sign_up_employee(message, service, date, empls):
    user_id = message.from_user.id
    choice = message.text
    if choice in empls:
        sign_up_time(message, service, date, choice)
    elif choice == design.menu_navigation[0]:
        sign_up_date(message, service)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_sign_up_employee, service, date, empls)

# Choose time to sign up
def sign_up_time(message, service, date, employee):
    user_id = message.from_user.id
    text = message.text
    times = get_available_time(service, date, employee)
    text = "Choose time below:"
    bot.send_message(user_id, text, parse_mode='html', reply_markup = design.keyboard(times, n_cols=3))
    bot.register_next_step_handler(message, process_sign_up_time, service, date, employee, times)

#
def process_sign_up_time(message, service, date, employee, times):
    user_id = message.from_user.id
    choice = message.text
    if choice in times:
        if sign_up(user_id, service, date, employee, choice):
            text = f"You successfully made an appointment.\n\n{date[:5]}, {choice}, {service}, {employee}"
            bot.send_message(user_id, text, parse_mode='html')
        else:
            text = "While scheduling an appointment something went wrong. Please try again."
            bot.send_message(user_id, text, parse_mode='html')
        menu.send_welcome(message)
    elif choice == design.menu_navigation[0]:
        sign_up_employee(message, service, date)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_sign_up_time, service, date, employee, times)

# ------Change appointments------

#
def change_appointment(message, app):
    user_id = message.from_user.id
    text = message.text
    text = f"Here is info about your appointment:\n\nDate: {app['date']}\nTime: {app['time']}"
    text += f"\nService: {services.get_service('id',app['service'],'name')}\nEmployee: {get_employee('id',app['employee'],'full_name')}"
    text += "\n\nChoose operation below:"
    options = ['Delete appointment','Reschedule appointment','Change employee']
    bot.send_message(user_id, text, parse_mode='html', reply_markup = design.keyboard(options, n_cols=3))
    bot.register_next_step_handler(message, process_change_appointment, app)

#
def process_change_appointment(message, app):
    user_id = message.from_user.id
    choice = message.text
    if choice == design.menu_navigation[0]:
        send_appointments(message)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    elif choice == "Delete appointment":
        delete_appointment(app['id'])
        text = "Appointment was successfully deleted"
        bot.send_message(user_id, text, parse_mode='html')
        menu.send_welcome(message)
    elif choice == "Reschedule appointment":
        change_appointment_date(message, app)
    elif choice == "Change employee":
        empls = get_available_employees(services.get_service('id',app['service'],'name'), app['date'], app['id'])
        bot.send_message(user_id, "Choose employee below:", parse_mode='html', reply_markup=design.keyboard(empls, n_cols=2))
        bot.register_next_step_handler(message, process_change_employee, app, empls)
    else:
        bot.register_next_step_handler(message, process_change_appointment, app)

#
def change_appointment_date(message, app):
    user_id = message.from_user.id
    text = message.text
    text = "Choose date below:"
    dates = get_available_date(services.get_service('id',app['service'],'name'), get_employee('id',app['employee'],'full_name'), app['id'])
    bot.send_message(user_id, text, parse_mode='html', reply_markup = design.keyboard(dates, n_cols=3))
    bot.register_next_step_handler(message, process_change_appointment_date, app, dates)

#
def process_change_appointment_date(message, app, dates):
    user_id = message.from_user.id
    choice = message.text
    if choice == design.menu_navigation[0]:
        change_appointment(message, app)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    elif choice in dates:
        change_appointment_time(message, app, choice)
    else:
        bot.register_next_step_handler(message, process_change_appointment_date, app, dates)

#
def change_appointment_time(message, app, date):
    user_id = message.from_user.id
    text = message.text
    text = "Choose time below:"
    times = get_available_time(services.get_service('id',app['service'],'name'), date, get_employee('id',app['employee'],'full_name'), app['id'])
    bot.send_message(user_id, text, parse_mode='html', reply_markup = design.keyboard(times, n_cols=3))
    bot.register_next_step_handler(message, process_change_appointment_time, app, date, times)

#
def process_change_appointment_time(message, app, date, times):
    user_id = message.from_user.id
    choice = message.text
    if choice == design.menu_navigation[0]:
        change_appointment_date(message, app)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    elif choice in times:
        sign_up(user_id, services.get_service('id',app['service'],'name'), date, get_employee('id',app['employee'],'full_name'), choice, app['id'])
        delete_appointment(app['id'])
        text = "Your appointment was successfully rescheduled."
        bot.send_message(user_id, text, parse_mode='html')
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_change_appointment_time, app, date, times)

#
def process_change_employee(message, app, empls):
    user_id = message.from_user.id
    choice = message.text
    if choice == design.menu_navigation[0]:
        change_appointment(message, app)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    elif choice in empls:
        con = sqlite3.connect(database)
        c = con.cursor()
        c.execute('UPDATE appointments SET employee=? WHERE app_id=?',
                  (get_employee('full_name',choice,'id'), app['id'],))
        con.commit()
        con.close()
        text = "Employee for your appointmnet was successfully changed."
        bot.send_message(user_id, text, parse_mode='html')
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_change_employee, app, empls)