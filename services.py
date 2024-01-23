import design
import sqlite3
import texts
import menu
import appointments
import registration

from credentials import bot, database

services = []
services_list = []

# Fill services
def update_services():
    con = sqlite3.connect(database)
    c = con.cursor()
    c.execute('SELECT * FROM services')
    data = c.fetchall()
    con.close()
    global services_buttons
    global services
    services = []
    if data != None:
        for element in data:
            info = {
            'id': element[0],
            'name': element[1],
            'info': element[2],
            'price': element[3],
            'time': element[4]
            }
            services.append(info)
            services_list.append(info['name'])
update_services()

#
def get_service(input_attr, value, output_attr=None):
    for srvc in services:
        if srvc[input_attr] == value:
            if output_attr is None:
                return srvc
            return srvc[output_attr]
    return None

# Services message
def send_services(message):
    user_id = message.from_user.id
    bot.send_message(user_id, texts.SERVICES, parse_mode='html', reply_markup = design.keyboard(services_list, n_cols=2))
    bot.register_next_step_handler(message, process_service_selection)

#
def process_service_selection(message):
    user_id = message.from_user.id
    choice = message.text
    if choice in services_list:
        send_service_info(message)
    elif choice == design.menu_navigation[0]:
        menu.send_welcome(message)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_service_selection)

#
def send_service_info(message):
    user_id = message.from_user.id
    text = message.text
    for srvc in services:
        if srvc['name'] == text:
            bot.send_message(user_id, srvc['info'], parse_mode='html', reply_markup = design.keyboard(["✍ Sign up for "+text]))
            bot.register_next_step_handler(message, process_signup_selection)
            return

#
def process_signup_selection(message):
    user_id = message.from_user.id
    choice = message.text
    if "✍ Sign up for " in choice and choice[14:] in services_list:
        data = registration.get_user_data(user_id)
        if data is not None:
            appointments.sign_up_date(message, choice[14:])
        else:
            text = "You are not registered. Let's get you registered!\nPlease share your phone number:"
            bot.send_message(user_id, text, reply_markup=design.keyboard(['Share your phone']))
            bot.register_next_step_handler(message, registration.process_phone_number)
    elif choice == design.menu_navigation[0]:
        send_services(message)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.register_next_step_handler(message, process_signup_selection)
