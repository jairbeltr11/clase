import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


from pyfirmata import Arduino, util
from tkinter import *
from PIL import Image
from PIL import ImageTk
import time
cont=0
prom=0

placa = Arduino ('COM8')
it = util.Iterator(placa)
it.start()
a_0 = placa.get_pin('a:0:i')
led1 = placa.get_pin('d:3:p')
led2 = placa.get_pin('d:5:p')
led3 = placa.get_pin('d:6:p')
led4 = placa.get_pin('d:9:p')
led5 = placa.get_pin('d:10:p')
led6 = placa.get_pin('d:11:p')
time.sleep(0.5)
ventana = Tk()
ventana.geometry('1280x800')
ventana.title("UI para sistemas de control")

# Fetch the service account key JSON file contents
cred = credentials.Certificate('keys/key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bdtkinter.firebaseio.com/'
})


marco1 = Frame(ventana, bg="gray", highlightthickness=1, width=1280, height=800, bd= 5)
marco1.place(x = 0,y = 0)
b=Label(marco1,text="")
img = Image.open("C:/Users/Camilo/Downloads/logousa.png")
img = img.resize((150,150), Image.ANTIALIAS)
photoImg=  ImageTk.PhotoImage(img)
b.configure(image=photoImg)
b.place(x = 760,y = 20)

valor= Label(marco1, bg='cadet blue1', font=("Arial Bold", 15), fg="white", width=5)
variable=StringVar()
valor2= Label(marco1, bg='cadet blue1', font=("Arial Bold", 15), fg="white", width=5)
adc_data=StringVar()

def update_label():
    global cont
    cont=cont+1
    ref = db.reference("sensor")
    ref.update({
                'sensor1': {
                    'adc': 0,
                    'valor': cont,
                    
            }
         })
    variable.set(cont)

def adc_read():
    global prom
    i=0
    prom=0
    while i<15:
        i=i+1
        x=a_0.read()
        print(x)
        adc_data.set(x)
        prom=x+prom
        ventana.update()
        time.sleep(0.1)
    prom=prom/15
    print("El promedio es ",prom)
    ref = db.reference('sensor')
    ref.update({
        'sensor2/adc': prom
    })

def save():
    ref = db.reference('sensor')
    ref.update({
        'sensor3/message': 'hola'
    })
    
    
  

valor.configure(textvariable=variable)
valor.place(x=20, y=90)
start_button=Button(marco1,text="cont",command=update_label)
start_button.place(x=20, y=160)

valor2.configure(textvariable=adc_data)
valor2.place(x=130, y=90)
start_button2=Button(marco1,text="adc_data",command=adc_read)
start_button2.place(x=80, y=160)

save_button=Button(marco1,text="save",command=save)
save_button.place(x=170, y=160)




ventana.mainloop()
