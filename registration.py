import telebot
import design
import sqlite3
import menu

from credentials import bot, database

# Function to get username from user_id
def get_username(user_id):
    '''
    try:
        user_info = bot.chat(user_id)
        return user_info.username
    except telebot.apihelper.ApiException as e:
        print(f"Error getting username for user_id {user_id}: {e}")
        return None
    '''
    return None

# User is registered, retrieve and display data
def get_user_data(user_id):
    con = sqlite3.connect(database)
    c = con.cursor()
    c.execute('SELECT full_name, phone FROM users WHERE user_id=?', (user_id,))
    data = c.fetchone()
    con.close()
    if data is None:
        return None
    return {
        'full_name': data[0],
        'phone': data[1]
    }

# Register a new user
def register_user(user_id, phone_number, full_name):
    con = sqlite3.connect(database)
    c = con.cursor()
    c.execute('INSERT INTO users (user_id, username, full_name, phone) VALUES (?, ?, ?, ?)',
              (user_id, get_username(user_id), full_name, phone_number))
    con.commit()
    con.close()

# Function to update user data
def update_user_data(user_id, phone_number, full_name):
    con = sqlite3.connect(database)
    c = con.cursor()
    if phone_number is not None:
        c.execute('UPDATE users SET username=?, phone=? WHERE user_id=?',
                  (get_username(user_id), phone_number, user_id))
    if full_name is not None:
        c.execute('UPDATE users SET username=?, full_name=? WHERE user_id=?',
                  (get_username(user_id), full_name, user_id))
    con.commit()
    con.close()

# -----Menu------

# Command handler to check user info
def send_profile(message):
    user_id = message.from_user.id
    data = get_user_data(user_id)
    if data is not None:
        phone = data['phone']
        full_name = data['full_name']
        text = f"Full name: {full_name}\nPhone Number: {phone}"
        bot.send_message(user_id, text, reply_markup=design.keyboard(design.menu_change_profile, n_cols=2))
        bot.register_next_step_handler(message, process_change_request)
    else:
        text = "You are not registered. Let's get you registered!\nPlease share your phone number:"
        bot.send_message(user_id, text, reply_markup=design.keyboard(['Share phone number']))
        #bot.send_message(user_id, text, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_phone_number)

# Function to handle user's phone number during registration
def process_phone_number(message):
    user_id = message.from_user.id
    phone_number = message.text
    if phone_number == design.menu_navigation[0]:
        menu.send_welcome(message)
    elif phone_number == design.menu_navigation[1]:
        menu.send_welcome(message)
    elif not phone_number.isdigit() or len(phone_number) != 10:
        bot.send_message(user_id, "Invalid phone number format. Please enter a valid 10-digit phone number.")
        bot.register_next_step_handler(message, process_phone_number)
    else:
        bot.send_message(user_id, "Great! Now, please share your full name:", reply_markup=design.keyboard())
        bot.register_next_step_handler(message, process_full_name, phone_number)

# Function to handle user's full name during registration
def process_full_name(message, phone_number):
    user_id = message.from_user.id
    full_name = message.text
    if full_name == design.menu_navigation[0]:
        send_profile(message)
    elif full_name == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        text = f"Phone Number: {phone_number}\nFull Name: {full_name}\n\nPlease confirm your registration:"
        bot.send_message(user_id, text, reply_markup=design.keyboard(["Confirm", "Cancel"]))
        bot.register_next_step_handler(message, process_registration_confirmation, phone_number, full_name)

# Function to handle user's confirmation or cancellation of registration
def process_registration_confirmation(message, phone_number, full_name):
    user_id = message.from_user.id
    choice = message.text
    if choice == "Confirm":
        register_user(user_id, phone_number, full_name)
        text = f"Registration complete! Your information:\nPhone Number: {phone_number}\nFull Name: {full_name}"
        bot.send_message(user_id, text, reply_markup=design.keyboard(design.menu_options,False,False))
        bot.register_next_step_handler(message, menu.process_menu_selection)
        #!!!
    elif choice == "Cancel":
        text = "Registration was canceled."
        bot.send_message(user_id, text)
        menu.send_welcome(message)
    elif choice == design.menu_navigation[0]:
        bot.send_message(user_id, "Great! Now, please share your full name:", reply_markup=design.keyboard())
        bot.register_next_step_handler(message, process_full_name, phone_number)
    elif choice == design.menu_navigation[1]:
        text = "Registration was canceled."
        bot.send_message(user_id, text)
        menu.send_welcome(message)
    else:
        bot.send_message(user_id, "Invalid choice. Please select a valid option.")
        bot.send_message(user_id, "Please confirm your registration:", reply_markup=design.keyboard(["Confirm", "Cancel"]))
        bot.register_next_step_handler(message, process_registration_confirmation, phone_number, full_name)

#------Change Profile Data------

# Function to handle change request
def process_change_request(message):
    user_id = message.from_user.id
    choice = message.text
    if choice == "Change Phone Number":
        bot.send_message(user_id, "Sure! Please share your new phone number:", reply_markup=design.keyboard(["Share phone"]))
        bot.register_next_step_handler(message, process_new_phone_number)
    elif choice == "Change Full Name":
        bot.send_message(user_id, "Sure! Please share your new full name:", reply_markup=design.keyboard())
        bot.register_next_step_handler(message, process_new_full_name)
    elif choice == design.menu_navigation[0]:
        menu.send_welcome(message)
    elif choice == design.menu_navigation[1]:
        menu.send_welcome(message)
    else:
        bot.send_message(user_id, "Invalid choice. Please select a valid option.")
        bot.register_next_step_handler(message, process_change_request)

# Function to handle phone number change
def process_new_phone_number(message):
    user_id = message.from_user.id
    new_phone_number = message.text
    if new_phone_number == design.menu_navigation[0]:
        send_profile(message)
        return
    elif new_phone_number == design.menu_navigation[1]:
        menu.send_welcome(message)
        return
    if not new_phone_number.isdigit() or len(new_phone_number) != 10:
        bot.send_message(user_id, "Invalid phone number format. Please enter a valid 10-digit phone number.")
        bot.register_next_step_handler(message, process_new_phone_number)
        return
    update_user_data(user_id, new_phone_number, None)
    bot.send_message(user_id, f"Phone number updated to: {new_phone_number}")
    send_profile(message)

# Function to handle new full name
def process_new_full_name(message):
    user_id = message.from_user.id
    new_full_name = message.text
    if new_full_name == design.menu_navigation[0]:
        send_profile(message)
        return
    elif new_full_name == design.menu_navigation[1]:
        menu.send_welcome(message)
        return
    update_user_data(user_id, None, new_full_name)
    bot.send_message(user_id, f"Full name updated to: {new_full_name}")
    send_profile(message)