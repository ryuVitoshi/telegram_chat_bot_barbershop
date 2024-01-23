import sqlite3

con = sqlite3.connect("superbarbershop.db")
c = con.cursor()

# USERS
c.execute('''CREATE TABLE IF NOT EXISTS users
             (user_id INTEGER PRIMARY KEY,
              username TEXT,
              full_name TEXT,
              phone TEXT)
              ''')

# EMPLOYEES
c.execute('''CREATE TABLE IF NOT EXISTS employees
             (employee_id INTEGER PRIMARY KEY,
              full_name TEXT,
              role TEXT,
              phone TEXT)
              ''')

c.execute('''INSERT INTO employees (full_name, role, phone) VALUES
             ('Andriy Melnikov','Owner','+380123456789'),
             ('Milana Pavun','Master hairdresser','+380987654321'),
             ('Pavlo Mazilo','Hairdresser','+380654321789');
             ''')

# SCHEDULE
c.execute('''CREATE TABLE IF NOT EXISTS schedule
             (schedule_id INTEGER PRIMARY KEY,
              employee INTEGER,
              date TEXT,
              start_time TEXT,
              shift_time REAL,
              FOREIGN KEY(employee) REFERENCES employees(employee_id))
              ''')

'''

c.execute( _ _ _ INSERT INTO schedule (employee, date, start_time, shift_time) VALUES
             (,'','',10),
             (,'','',8),
             (,'','',10),
             (,'','',8),
             (,'','',6),
             (,'','',6),
             (,'','',6);
             _ _ _)

'''
             
# SERVICES
c.execute('''CREATE TABLE IF NOT EXISTS services
             (service_id INTEGER PRIMARY KEY,
              service_name TEXT,
              service_info TEXT,
              price REAL,
              time REAL)
              ''')

c.execute('''INSERT INTO services (service_name, service_info, price, time) VALUES
             ('Master cut','Begins with a shampoo done with revitalizing hair wash proceeds to your cut and style of choice. Finishes with eyebrows shaping and straight razor neck shave and hot towel with eucalyptus freeze splash.',60,60),
             ('Master long hair','Any cut that is desired to be left longer than 6 inches at the end of the service.',75,60),
             ('Master beard trim','Begins with shaping and trimming of your choice. Continues with towel inundation, skin hydration via steam machine, and a one-directional razor shave. Finishes with a cold towel to prevent infection, toner and aftershave to protect the skin. Punctuality and satisfaction guaranteed or you pay nothing.',40,40),
             ('Master shave','Begins with shaping of whatever facial is to remain and an in-depth skin consultation. Continues with in-house shaving cream applied with vegan silvertip badger hair brush. Double towel inundation leads into the first pass that is completed with the grain of the hair growth as the face is hydrated by a steam machine. The steaming continues through the second pass after lather is replied for maximum exfoliation of the skin. Finishes with cold towel and in-house aftershave serum. This service includes shaping over your ears as well as a neck shave.',50,60),
             ('Master head shave','Begins with in house shaving cream applied with vegan silvertip badger hair brush followed by double hot towel inundation. Continues with a two-directional shave of head and back of the neck, finishes with a cold towel to prevent infection and toner and aftershave to protect the skin.',50,40),
             ('Buzz cut','One level even trim all the way around with the clipper. Finishes with the trimmer and razor line up + hot towel neck shave. Does not include, tapering, blending, or fading of any sort.',30,30),
             ('Kids cut','Your childs cut and style of choice executed with the precise hand of the barber of your choice. Please note: This is for children 12 and under and does NOT include a design of any sort. Please kindly book a design under the "haircut add-ons" section if you desire a design of any sort.',40,30),
             ('Braids','Braids are $100 an hour w/ a one hour minimum. Please call for a consultation before booking as we like to treat each braiding service as unique occurrence and take each client case by case.',100,60);
             ''')

# APPOINTMENTS
c.execute('''CREATE TABLE IF NOT EXISTS appointments
             (app_id INTEGER PRIMARY KEY,
              app_date TEXT,
              app_time TEXT,
              comment TEXT,
              user INTEGER,
              service INTEGER,
              employee INTEGER,
              FOREIGN KEY(user) REFERENCES users(user_id),
              FOREIGN KEY(service) REFERENCES services(service_id),
              FOREIGN KEY(employee) REFERENCES employees(employee_id)
              )''')

con.commit()
