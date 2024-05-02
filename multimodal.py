import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import recognition
import mail
import mysql.connector as mq
from mysql.connector import Error
import pyttsx3
import random
import serial
import time
engine = pyttsx3.init()
face=False
otpval=False
passw=False
otp=0
rxemail=""


# Define the serial port and baudrate
serial_port = 'COM4'  # Change this to your serial port
baudrate = 9600  # Change this to match your device's baudrate

def dbconnection():
    con = mq.connect(host='localhost', database='multi',user='root',password='root')
    return con

def verify_face():
    global face
    global rxemail
    res = recognition.detectPerson()
    print("email is :",res)
    # Placeholder function for face verification
    if res!="failed":
        face=True
        rxemail=res.strip()
        result_text.set("Face verification success")
        engine.say("Face verified")
        engine.runAndWait()
        
    else:
        result_text.set("Face verification Failed")
        engine.say("Face verification Failed")
        engine.runAndWait()
    # Placeholder for failed verification
    # result_text.set("Authentication failed")

def send_otp():
    global otp
    # Generate a random 6-digit OTP
    otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    print(rxemail)
    mail.send_otp_email(otp,rxemail)
    # Placeholder function for sending OTP

def verify_otp():
    global otpval
    print("inside otp verification")
    entered_text = otp_entry.get()
    if entered_text.strip() == otp:
        otpval=True
        result_text.set("OTP verified")
        engine.say("OTP verified")
        engine.runAndWait()
    else:
        result_text.set("Failed Incorrect OTP")
        engine.say("OTP verification failed")
        engine.runAndWait()
    # Placeholder for failed verification
    # result_text.set("Verification failed")

def verify_password():
    global passw
    psw=password_entry.get()
    con = dbconnection()
    cursor = con.cursor()
    cursor.execute("select * from users where email='{}' and pass='{}'".format(rxemail,psw.strip()))
    res = cursor.fetchall()
    if res==[]:
        result_text.set("Incorrect password")
        engine.say("Incorrect Password")
        engine.runAndWait()
    else:
        passw=True
        engine.say("Password verified, place you finger on fingerprint device and press authenticate fingerprint button")
        engine.runAndWait()
        result_text.set("Password verified")

def authenticate_fingerprint():
    print(face,otpval,passw)
    # Placeholder function for fingerprint authentication
    if face==True and otpval==True and passw==True:
        result_text.set("Authenticate your fingerprint")
        try:
            # Open the serial port
            ser = serial.Serial(serial_port, baudrate)

            # Wait for the serial connection to be established
            time.sleep(2)

            # Send data
            data_to_send = b'1'  # Convert string '1' to bytes
            ser.write(data_to_send)
            print("Data sent successfully.")

            # Close the serial port
            ser.close()

        except serial.SerialException as e:
            print("Serial port error:", e)
            result_text.set("Serial port error")
        except Exception as e:
            print("Error:", e)
            result_text.set("error communicating")
    else:
        result_text.set("You have not passed all the verifications")
        engine.say("You have not passed all the verifications")
        engine.runAndWait()
        

root = tk.Tk()
root.title("Multimodal Authentication System")

# Load background image
background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Set background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

header_label = tk.Label(root, text="MULTIMODULE AUTHENTICATION SYSTEM", font=("Arial", 20,"bold"))
header_label.pack(pady=20)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, font=("Arial", 16,"bold"), fg="red")
result_label.pack(pady=20)

verify_face_button = tk.Button(root, text="VERIFY FACE",width=20, command=verify_face, font=("Arial", 12, "bold"))
verify_face_button.pack(pady=10)



send_otp_button = tk.Button(root, text="SEND OTP",width=20, command=send_otp, font=("Arial", 12, "bold"))
send_otp_button.pack(pady=10)

otp_entry = tk.Entry(root, width=30)
otp_entry.pack(pady=10)

verify_otp_button = tk.Button(root, text="VERIFY OTP",width=20, command=verify_otp, font=("Arial", 12, "bold"))
verify_otp_button.pack(pady=10)

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=10)

verify_password_button = tk.Button(root, text="VERIFY PASSWORD",width=20, command=verify_password, font=("Arial", 12, "bold"))
verify_password_button.pack(pady=10)

fingerprint_button = tk.Button(root, text="VERIFY FINGERPRINT",width=20, command=authenticate_fingerprint, font=("Arial", 12, "bold"))
fingerprint_button.pack(pady=10)

root.mainloop()
