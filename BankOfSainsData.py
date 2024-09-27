import tkinter as tk
from tkinter import ttk
import smtplib
from email.mime.text import MIMEText
import datetime
from tkinter import *
import random
from PIL import ImageTk, Image
import locale
import time
import pymongo
from bson import ObjectId
from pymongo import MongoClient
import os
import sys
import hashlib
import ctypes
from cryptography.fernet import Fernet

def resource_path(relative_path):
    '''untuk mengakses asset seperti images'''
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def decryption():
    with open('key.key', 'rb') as key_file:
        key = key_file.read()

    with open('config.enc', 'rb') as enc_file:
        encrypted_password = enc_file.read()

    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password).decode()

    return decrypted_password

class BankSainsData:
    def __init__(self, bsd):
        self.bsd = bsd
        self.login_username = None
        self.click_count = 0
        self.no_reke = 0
        self.nominal_tf = 0
        self.myRekening= 0

        self.bsd.title('BSD')
        self.bsd.geometry('1280x720')
        self.bsd.state('zoomed')
        self.bsd.attributes('-fullscreen', True)

        bg_image = Image.open("images\Frame 25 (2).png")
        resize_imge = bg_image.resize((1280, 720))

        self.photo = ImageTk.PhotoImage(resize_imge)
        self.lbl = tk.Label(bsd,image=self.photo)
        self.image = self.photo
        self.lbl.place(x=0,y=0)
        self.bsd.configure(bg='#333333')

        passDB = decryption()
        self.client = MongoClient(passDB)
        self.db = self.client['Bank_Sains_Data']

        self.data_user = self.db['database_client_BSD']

        self.transaction_history = self.db['transaction_history']

        def quitApp():
            self.frame_quit = tk.Frame(self.bsd)
            self.frame_quit.place(x=380, y=270)

            bg3_image = Image.open("images\Frame 52.png")
            resize_image = bg3_image.resize((520, 226))
            self.photo2 = ImageTk.PhotoImage(resize_image)

            self.lbl_frame = tk.Label(self.frame_quit, image=self.photo2)
            self.lbl_frame.image = self.photo2
            self.lbl_frame.pack()

            def quitBSD():
                self.frame_quit.destroy()
                self.client.close()
                self.bsd.destroy()
                self.bsd.quit()
            def stayBSD():
                self.frame_quit.destroy()

            self.yessbutt = tk.Button(self.frame_quit,
                                     font=('Helvetica',18,'bold'),
                                     text="Iya",
                                     fg="black",
                                     bg="#ffa41c",
                                     border=0,
                                     activebackground="#ffa41c",
                                     activeforeground="black",
                                     cursor="hand2",
                                     width=10,
                                     command=quitBSD)
            self.yessbutt.place(x=297, y=140)
            self.noobutt = tk.Button(self.frame_quit,
                                     font=('Helvetica',18,'bold'),
                                     text="Tidak",
                                     fg="black",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="black",
                                     cursor="hand2",
                                     width=10,
                                     command=stayBSD)
            self.noobutt.place(x=75, y=140)
    

        self.userframe = tk.Frame(bsd,bg='#F1F1F1')
        self.userframe.place(x=490, y=252)

        self.outframe = tk.Frame(bsd,bg='#F1F1F1')
        self.outframe.place(x=1140, y=13)

        self.passframe = tk.Frame(bsd,bg="#F1F1F1")
        self.passframe.place(x=490,y=303)

        self.loginframe = tk.Frame(bsd,bg="#F1F1F1")
        self.loginframe.place(x=480,y=370)

        self.regframe = tk.Frame(bsd,bg="#F1F1F1")
        self.regframe.place(x=480,y=475)

        self.klikframe=tk.Frame(bsd,bg='#FDCB7F')
        self.klikframe.place(x=740,y=535)

        def enter_namebutton(e):
            name = self.username_entry.get()
            if name == "Username":
                self.username_entry.delete(0, 'end')

        def leave(e):
            name = self.username_entry.get()
            if name == "":
                self.username_entry.insert(0,"Username")

        def enter_passButton(e):
            passw = self.password_entry.get()
            if passw == "Password":
                self.password_entry.delete(0, "end")

        def leave_passButton(e):
            passw = self.password_entry.get()
            if passw == "":
                self.password_entry.insert(0, "Password")

        self.username_entry = tk.Entry(self.userframe,
                                       font=('Helvetica', 20),
                                       fg="black",
                                       bg="#ffffff",
                                       border=0,
                                       width=17)
        self.username_entry.pack()
        self.username_entry.insert(0,"Username")
        self.username_entry.bind('<FocusIn>', enter_namebutton)
        self.username_entry.bind('<FocusOut>', leave)

        self.password_entry = tk.Entry(self.passframe,
                                       font=('Helvetica', 20),
                                       fg="black",
                                       bg="#ffffff",
                                       border=0,
                                       width=17)
        self.password_entry.pack()
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', enter_passButton)
        self.password_entry.bind('<FocusOut>', leave_passButton)

        self.register = tk.Button(self.regframe,
                                  text='DAFTAR',
                                  font=("Helvetica",18),
                                  bg="#FDCB7F",
                                  fg="#ffffff",
                                  cursor="hand2",
                                  border=0,
                                  command=self.signup,
                                  width=23,
                                  activebackground = "#FDCB7F",
                                  activeforeground = "#ffffff",)
        self.register.pack()

        self.login_button = tk.Button(self.loginframe,
                                       text='MASUK',
                                       font=("Helvetica",18),
                                       command=self.login,
                                       fg="#ffffff",
                                      bg="#FDCB7F",
                                      width=23,
                                      border=0,
                                      activebackground="#FDCB7F",
                                      activeforeground="#ffffff",
                                      cursor="hand2")
        self.login_button.grid()

        self.forgot_button = tk.Button(self.klikframe,
                                       text='Klik',
                                       font=("Helvetica",10),
                                       command=self.forgot,
                                       fg="black",
                                      bg="#FDCB7F",
                                      width=8,
                                      border=0,
                                      activebackground="#FDCB7F",
                                      activeforeground="black",
                                      cursor="hand2")
        self.forgot_button.grid()

        self.outApp = tk.Button(self.outframe,text='QUIT',
                                 font=("Helvetica", 15),
                                 command=quitApp,
                                 fg="#ffffff",
                                 bg="#E4B672",
                                 border=0,
                                 activebackground="#E4B672",
                                 activeforeground="#ffffff",
                                 cursor="hand2",
                                 width=11)
        self.outApp.pack()

    def set_taskbar_icon(self):
        if getattr(sys, 'frozen', False):
            application_path = sys.executable
        else:
            application_path = os.path.abspath(__file__)

        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        icon_path = os.path.join(os.path.dirname(application_path), "images\BSDLogo.ico")
        self.bsd.iconbitmap(default=icon_path)

    def forgot(self):
        self.forgot = Toplevel(self.bsd)
        self.forgot.title('BSD')
        self.forgot.geometry('1280x720')
        self.forgot.attributes('-fullscreen', True)
        bg_image = Image.open("images\Frame 58.png")
        resize_imge = bg_image.resize((1280, 720))
        photo2 = ImageTk.PhotoImage(resize_imge)
        self.lbl2 = tk.Label(self.forgot, image=photo2)
        self.lbl2.place(x=0, y=0)
        self.forgot.configure(bg="#333333")

        def out_from_forgot():
            self.forgot.destroy()
            self.bsd.deiconify()

        def usernameNEW_textt(e):
            userNEW = self.usernameNEW_create.get()
            if userNEW =="Username":
                self.usernameNEW_create.delete(0, "end")

        def NEWzoomout(e):
            nameNEW = self.usernameNEW_create.get()
            if nameNEW == "":
                self.usernameNEW_create.insert(0,"Username")

        def passwordNEW_textt(e):
            passwNEW = self.passwordNEW_create.get()
            if passwNEW == "Password Baru":
                self.passwordNEW_create.delete(0,"end")

        def passwordNEW_zoomout(e):
            namesNEW = self.passwordNEW_create.get()
            if namesNEW == "":
                self.passwordNEW_create.insert(0,"Password Baru")
        #
        def pinNEW_text(e):
            pinNEW = self.pinNEW_create.get()
            if pinNEW == "PIN Baru":
                self.pinNEW_create.delete(0,"end")
        #
        def pinNEW_zoomout(e):
            nameNEW = self.pinNEW_create.get()
            if nameNEW == "":
                self.pinNEW_create.insert(0,"PIN Baru")
                
        def norekNEW_text(e):
            nimNEW = self.norekNEW_create.get()
            if nimNEW == "NIM":
                self.norekNEW_create.delete(0,"end")
        #
        def norekNEW_zoomout(e):
            nameNEW = self.norekNEW_create.get()
            if nameNEW == "":
                self.norekNEW_create.insert(0,"NIM")

        def lanjut():
            usernameNew = self.usernameNEW_create.get()
            norekNew = self.norekNEW_create.get()
            passwordNew = self.hashingFunction(self.passwordNEW_create.get())
            pinNew = self.pinNEW_create.get()
            pinNew = str(pinNew)

            rowForgot = self.data_user.find_one({"username":usernameNew, "nomor_rekening":norekNew})

            if rowForgot is not None:
                email_tujuan = rowForgot.get("email")
                if passwordNew is not None and pinNew.isdigit() and passwordNew!='Password Baru' and len(pinNew) == 6:
                    bg3_image = Image.open("images\Frame 59 (1).png")
                    resize_image = bg3_image.resize((355, 139))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.frame_check = tk.Frame(self.forgot)
                    self.frame_check.place(x=470, y=270)

                    self.lbc_frame = tk.Label(self.frame_check, image=self.photo2)
                    self.lbc_frame.image = self.photo2
                    self.lbc_frame.pack()

                    def left_pin_check():
                        self.frame_check.destroy()

                    def otp_button():
                        self.frame_check.destroy()
                        name = self.usernameNEW_create.get()
                        otpCODE = str(random.randint(000000, 999999))

                        if email_tujuan != "Email" and email_tujuan is not None and "@gmail.com" in email_tujuan:
                            email_penerima = str(email_tujuan)
                            sender_email = "bankofsainsdata23@gmail.com"
                            app_password = "behc alss xujn orbw"
                            subject = "Konfirmasi Kode OTP untuk Akses Akun Anda"

                            message = MIMEText(
                                f" Dear {name}\n\nKami ingin mengkonfirmasi bahwa Anda telah"
                                f" meminta untuk menerima kode OTP untuk mengakses akun Anda."
                                f" Berikut adalah detail kode OTP 6 digit PIN yang dapat Anda gunakan:\n\n"
                                f"Kode OTP: {otpCODE}\n\nSalam Hangat dari Admin Bank Sains Data.\n\nTerima kasih.")
                            message["Subject"] = subject
                            message["From"] = sender_email
                            message["To"] = email_penerima

                            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                                server.starttls()
                                server.login(sender_email, app_password)
                                server.sendmail(sender_email, [email_penerima], message.as_string())

                            bg3_image = Image.open("images\Frame 60 (2).png")
                            resize_image = bg3_image.resize((211, 293))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.frame_otp = tk.Frame(self.forgot)
                            self.frame_otp.place(x=590, y=270)

                            self.lbc_frame = tk.Label(self.frame_otp, image=self.photo2)
                            self.lbc_frame.image = self.photo2
                            self.lbc_frame.pack()

                            def buttonc1():
                                self.pinc_entry.insert(tk.END, 1)

                            def buttonc2():
                                self.pinc_entry.insert(tk.END, 2)

                            def buttonc3():
                                self.pinc_entry.insert(tk.END, 3)

                            def buttonc4():
                                self.pinc_entry.insert(tk.END, 4)

                            def buttonc5():
                                self.pinc_entry.insert(tk.END, 5)

                            def buttonc6():
                                self.pinc_entry.insert(tk.END, 6)

                            def buttonc7():
                                self.pinc_entry.insert(tk.END, 7)

                            def buttonc8():
                                self.pinc_entry.insert(tk.END, 8)

                            def buttonc9():
                                self.pinc_entry.insert(tk.END, 9)

                            def buttonc0():
                                self.pinc_entry.insert(tk.END, 0)

                            def hapusc111():
                                self.pinc_entry.delete(0, tk.END)

                            def left_pin_c():
                                self.frame_otp.destroy()

                            def submit_checkOTP():
                                codeOTP = self.pinc_entry.get()
                                if codeOTP == otpCODE:
                                    self.data_user.update_one({"username":usernameNew},{'$set':{"password":passwordNew, "pin":pinNew}})
                                    self.forgot.destroy()
                                    self.forgot.quit()
                                    self.bsd.deiconify()
                                    self.frame_otp.destroy()
                                else:
                                    self.frame_9 = tk.Frame(self.forgot)
                                    self.frame_9.place(x=520, y=270)

                                    bg3_image = Image.open("images\Frame 62.png")
                                    resize_image = bg3_image.resize((219, 227))
                                    self.photo2 = ImageTk.PhotoImage(resize_image)

                                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                    self.lbl_frame.image = self.photo2
                                    self.lbl_frame.pack()

                                    def oouutt():
                                        self.frame_9.destroy()

                                    self.outbut9 = tk.Button(self.frame_9,
                                                             font=('Helvetica'),
                                                             text="x",
                                                             fg="#ffffff",
                                                             bg="#FDCB7F",
                                                             border=0,
                                                             activebackground="#FDCB7F",
                                                             activeforeground="#ffffff",
                                                             cursor="hand2",
                                                             width=3,
                                                             command=oouutt)
                                    self.outbut9.place(x=175, y=7)

                            self.pinc_entry = tk.Entry(self.frame_otp,
                                                       font=('Helvetica', 16, 'bold'), width=12,
                                                       border=0,
                                                       bg="#d9d9d9")
                            self.pinc_entry.place(x=40, y=52)

                            self.leftc_button = tk.Button(self.frame_otp, text="X",
                                                          font=('Helvetica', 10, 'bold'),
                                                          activebackground="#e4b672",
                                                          activeforeground="white", bg="#e4b672",
                                                          fg="white", border=0,
                                                          command=left_pin_c)
                            self.leftc_button.place(x=186, y=13)

                            self.buttonc1 = tk.Button(self.frame_otp, text="1",
                                                      font=('Helvetica', 13, 'bold'), bg="#d9d9d9",
                                                      border=0,activebackground="#d9d9d9",
                                                      command=buttonc1)
                            self.buttonc1.place(x=47, y=97)

                            self.buttonc2 = tk.Button(self.frame_otp, text="2",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      bg="#d9d9d9",activebackground="#d9d9d9",
                                                      command=buttonc2)
                            self.buttonc2.place(x=97, y=97)

                            self.buttonc3 = tk.Button(self.frame_otp, text="3",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      bg="#d9d9d9",activebackground="#d9d9d9",
                                                      command=buttonc3)
                            self.buttonc3.place(x=147, y=95)

                            self.buttonc4 = tk.Button(self.frame_otp, text="4",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      command=buttonc4)
                            self.buttonc4.place(x=47, y=140)

                            self.buttonc5 = tk.Button(self.frame_otp, text="5",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      command=buttonc5)
                            self.buttonc5.place(x=97, y=140)

                            self.buttonc6 = tk.Button(self.frame_otp, text="6",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      command=buttonc6)
                            self.buttonc6.place(x=147, y=140)

                            self.buttonc7 = tk.Button(self.frame_otp, text="7",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      command=buttonc7)
                            self.buttonc7.place(x=47, y=185)

                            self.buttonc8 = tk.Button(self.frame_otp, text="8",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      command=buttonc8)
                            self.buttonc8.place(x=97, y=185)

                            self.buttonc9 = tk.Button(self.frame_otp, text="9",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      command=buttonc9)
                            self.buttonc9.place(x=147, y=185)

                            self.buttonc0 = tk.Button(self.frame_otp, text="0",
                                                      font=('Helvetica', 13, 'bold'), border=0,
                                                      command=buttonc0)
                            self.buttonc0.place(x=97, y=230)

                            self.button_hapusc = tk.Button(self.frame_otp, text="⬅",
                                                           font=('Helvetica', 16, 'bold'), border=0,
                                                           activebackground="#e4b672",
                                                           activeforeground="white", bg="#e4b672",
                                                           fg="white",
                                                           command=hapusc111)
                            self.button_hapusc.place(x=29, y=240)

                            self.button_submitc = tk.Button(self.frame_otp, text="✅",
                                                            font=('Helvetica', 16, 'bold'),
                                                            border=0,
                                                            bg="#FDCB7F", fg="white",
                                                            activebackground="#FDCB7F",
                                                            activeforeground="white",
                                                            command=submit_checkOTP
                                                            )
                            self.button_submitc.place(x=140, y=240)

                        else:
                            self.frame_9 = tk.Frame(self.forgot)
                            self.frame_9.place(x=520, y=270)

                            bg3_image = Image.open("images\Frame 63.png")
                            resize_image = bg3_image.resize((219, 227))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            def oouutt():
                                self.frame_9.destroy()

                            self.outbut9 = tk.Button(self.frame_9,
                                                     font=('Helvetica'),
                                                     text="x",
                                                     fg="#ffffff",
                                                     bg="#FDCB7F",
                                                     border=0,
                                                     activebackground="#FDCB7F",
                                                     activeforeground="#ffffff",
                                                     cursor="hand2",
                                                     width=3,
                                                     command=oouutt)
                            self.outbut9.place(x=175, y=6)

                    self.leftcheck_button = tk.Button(self.frame_check, text="X",
                                                      font=('Helvetica', 10, 'bold'),
                                                      activebackground="#fdcb7f",
                                                      activeforeground="white", bg="#fdcb7f",
                                                      fg="white", border=0,
                                                      command=left_pin_check)
                    self.leftcheck_button.place(x=340, y=8)

                    self.button_otp = tk.Button(self.frame_check, text="Lanjutkan",
                                                font=('Helvetica', 14, 'bold'), bg="#ffa41c",
                                                fg='black',
                                                border=0, width=10, activebackground="#ffa41c",
                                                activeforeground="black",
                                                command=otp_button)
                    self.button_otp.place(x=120, y=78)
                elif len(pinNew) != 6:
                    self.frame_9 = tk.Frame(self.forgot)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 67.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                    self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.forgot)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 66.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                    self.outbut9.place(x=175, y=7)
            else:
                self.frame_9 = tk.Frame(self.forgot)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 64.png")
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                self.outbut9.place(x=175, y=7)
        
        self.usernameNEW_create = tk.Entry(self.forgot,
                                        font=('Helvetica', 20),
                                        fg="black",
                                        bg="#ffffff",
                                        border=0,
                                        width=17)
        self.usernameNEW_create.place(x=490, y=255)
        self.usernameNEW_create.insert(0, "Username")
        self.usernameNEW_create.bind('<FocusIn>', usernameNEW_textt)
        self.usernameNEW_create.bind('<FocusOut>', NEWzoomout)

        self.passwordNEW_create = tk.Entry(self.forgot,
                                        font=('Helvetica', 20),
                                        fg="black",
                                        bg="#ffffff",
                                        border=0,
                                        width=17)
        self.passwordNEW_create.place(x=490, y=357)
        self.passwordNEW_create.insert(0, "Password Baru")
        self.passwordNEW_create.bind('<FocusIn>', passwordNEW_textt)
        self.passwordNEW_create.bind('<FocusOut>', passwordNEW_zoomout)

        self.pinNEW_create = tk.Entry(self.forgot,
                                   font=('Helvetica', 20),
                                   fg="black",
                                   bg="#ffffff",
                                   border=0,
                                   width=17)
        self.pinNEW_create.place(x=490, y=407)
        self.pinNEW_create.insert(0, "PIN Baru")
        self.pinNEW_create.bind('<FocusIn>', pinNEW_text)
        self.pinNEW_create.bind('<FocusOut>', pinNEW_zoomout)

        self.norekNEW_create = tk.Entry(self.forgot,
                                     font=('Helvetica', 20),
                                     fg="black",
                                     bg="#ffffff",
                                     width=17,
                                     border=0)
        self.norekNEW_create.place(x=490, y=307)
        self.norekNEW_create.insert(0, "NIM")
        self.norekNEW_create.bind('<FocusIn>', norekNEW_text)
        self.norekNEW_create.bind('<FocusOut>', norekNEW_zoomout)

        self.lanjut_button= tk.Button(self.forgot,
                                text='Lanjutkan',
                                font=("Helvetica", 18),
                                command=lanjut,
                                 fg="black",
                                 bg="#FDCB7F",
                                 width=23,
                                 border=0,
                                 activebackground="#FDCB7F",
                                 activeforeground="black",
                                 cursor="hand2")
        self.lanjut_button.place(x=473, y=469)

        self.keluar_button = tk.Button(self.forgot,
                                text='Keluar',
                                font=("Helvetica", 18),
                                command=out_from_forgot,
                                 fg="black",
                                 bg="#FDCB7F",
                                 width=23,
                                 border=0,
                                 activebackground="#FDCB7F",
                                 activeforeground="black",
                                 cursor="hand2")
        self.keluar_button.place(x=473, y=532)

        self.forgot.mainloop()

    def hashingFunction(self, input_string):
        shaSign = hashlib.sha3_256(input_string.encode('utf-8')).hexdigest()
        return shaSign

    def signup(self):
        self.roots = Toplevel(self.bsd)
        self.roots.title('BSD')
        self.roots.geometry('1280x720')
        self.roots.attributes('-fullscreen', True)
        bg_image = Image.open("images\Frame 12 (5).png")
        resize_imge = bg_image.resize((1280, 720))
        photo2 = ImageTk.PhotoImage(resize_imge)
        self.lbl2 = tk.Label(self.roots, image=photo2)
        self.lbl2.place(x=0, y=0)
        self.roots.configure(bg="#333333")

        def signup_button():
            self.bsd.iconify()
            usernamee = self.username_create.get()
            passwordd = self.hashingFunction(self.password_create.get())
            pinn = self.pin_create.get()
            norekk = self.norek_create.get()
            depoo = self.depo_create.get()
            emaill = self.email_create.get()

            row_username = self.data_user.find_one({'username':usernamee})

            if checkbox_var.get():
                if row_username is None and usernamee!='Username':
                    if passwordd.isalnum():
                        if pinn.isdigit() and len(str(pinn)) == 6 :

                            row_norek = self.data_user.find_one({'nomor_rekening':norekk})

                            if norekk.isdigit() and len(str(norekk)) == 11 and row_norek is None:
                                if depoo.isdigit() and int(depoo) >= 150000:
                                    RNG = random.randint(100000000000, 999999999999)
                                    formatted_number = f'{RNG:012}'
                                    RNGG = '-'.join([formatted_number[i:i + 4] for i in range(0, len(formatted_number), 4)])
                                    if RNGG:
                                        if __name__ == "__main__":
                                            bg3_image = Image.open("images\Frame 59 (1).png")
                                            resize_image = bg3_image.resize((355, 139))
                                            self.photo2 = ImageTk.PhotoImage(resize_image)

                                            self.frame_check = tk.Frame(self.roots)
                                            self.frame_check.place(x=470, y=270)

                                            self.lbc_frame = tk.Label(self.frame_check, image=self.photo2)
                                            self.lbc_frame.image = self.photo2
                                            self.lbc_frame.pack()

                                            def left_pin_check():
                                                self.frame_check.destroy()

                                            def otp_button():
                                                self.frame_check.destroy()
                                                name = self.username_create.get()
                                                email_tujuan = self.email_create.get()
                                                otpCODE = str(random.randint(100000, 999999))

                                                if email_tujuan != "Email" and email_tujuan is not None and "@gmail.com" in email_tujuan:
                                                    email_penerima = str(email_tujuan)
                                                    sender_email = "bankofsainsdata23@gmail.com"
                                                    app_password = "behc alss xujn orbw"
                                                    subject = "Konfirmasi Kode OTP untuk Akses Akun Anda"

                                                    message = MIMEText(
                                                        f" Dear {name}\n\nKami ingin mengkonfirmasi bahwa Anda telah"
                                                        f" meminta untuk menerima kode OTP untuk mengakses akun Anda."
                                                        f" Berikut adalah detail kode OTP 6 digit PIN yang dapat Anda gunakan:\n\n"
                                                        f"Kode OTP: {otpCODE}\n\nSalam Hangat dari Admin Bank Sains Data.\n\nTerima kasih.")
                                                    message["Subject"] = subject
                                                    message["From"] = sender_email
                                                    message["To"] = email_penerima

                                                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                                                        server.starttls()
                                                        server.login(sender_email, app_password)
                                                        server.sendmail(sender_email, [email_penerima], message.as_string())

                                                    bg3_image = Image.open("images\Frame 60 (2).png")
                                                    resize_image = bg3_image.resize((211, 293))
                                                    self.photo2 = ImageTk.PhotoImage(resize_image)

                                                    self.frame_otp = tk.Frame(self.roots)
                                                    self.frame_otp.place(x=590, y=270)

                                                    self.lbc_frame = tk.Label(self.frame_otp, image=self.photo2)
                                                    self.lbc_frame.image = self.photo2
                                                    self.lbc_frame.pack()

                                                    def buttonc1():
                                                        self.pinc_entry.insert(tk.END, 1)

                                                    def buttonc2():
                                                        self.pinc_entry.insert(tk.END, 2)

                                                    def buttonc3():
                                                        self.pinc_entry.insert(tk.END, 3)

                                                    def buttonc4():
                                                        self.pinc_entry.insert(tk.END, 4)

                                                    def buttonc5():
                                                        self.pinc_entry.insert(tk.END, 5)

                                                    def buttonc6():
                                                        self.pinc_entry.insert(tk.END, 6)

                                                    def buttonc7():
                                                        self.pinc_entry.insert(tk.END, 7)

                                                    def buttonc8():
                                                        self.pinc_entry.insert(tk.END, 8)

                                                    def buttonc9():
                                                        self.pinc_entry.insert(tk.END, 9)

                                                    def buttonc0():
                                                        self.pinc_entry.insert(tk.END, 0)

                                                    def hapusc111():
                                                        self.pinc_entry.delete(0, tk.END)

                                                    def left_pin_c():
                                                        self.frame_otp.destroy()

                                                    def submit_checkOTP():
                                                        codeOTP = self.pinc_entry.get()
                                                        format_email = str(email_tujuan)
                                                        if codeOTP == otpCODE:
                                                            self.data_user.insert_one({
                                                                "username": usernamee,
                                                                "password": passwordd,
                                                                "balance": int(depoo),
                                                                "pin": pinn,
                                                                "nomor_rekening": norekk,
                                                                "nomor_kartu": RNGG,
                                                                "email": format_email})
                                                            self.roots.destroy()
                                                            self.roots.quit()
                                                            self.bsd.deiconify()
                                                            self.frame_otp.destroy()
                                                        else:
                                                            self.frame_9 = tk.Frame(self.roots)
                                                            self.frame_9.place(x=520, y=270)

                                                            bg3_image = Image.open("images\Frame 62.png")
                                                            resize_image = bg3_image.resize((219, 227))
                                                            self.photo2 = ImageTk.PhotoImage(resize_image)

                                                            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                                            self.lbl_frame.image = self.photo2
                                                            self.lbl_frame.pack()

                                                            def oouutt():
                                                                self.frame_9.destroy()

                                                            self.outbut9 = tk.Button(self.frame_9,
                                                                                     font=('Helvetica'),
                                                                                     text="x",
                                                                                     fg="#ffffff",
                                                                                     bg="#FDCB7F",
                                                                                     border=0,
                                                                                     activebackground="#FDCB7F",
                                                                                     activeforeground="#ffffff",
                                                                                     cursor="hand2",
                                                                                     width=3,
                                                                                     command=oouutt)
                                                            self.outbut9.place(x=175, y=7)

                                                    self.pinc_entry = tk.Entry(self.frame_otp,
                                                                               font=('Helvetica', 16, 'bold'), width=12,
                                                                               border=0,
                                                                               bg="#d9d9d9")
                                                    self.pinc_entry.place(x=40, y=52)

                                                    self.leftc_button = tk.Button(self.frame_otp, text="X",
                                                                                  font=('Helvetica', 10, 'bold'),
                                                                                  activebackground="#e4b672",
                                                                                  activeforeground="white", bg="#e4b672",
                                                                                  fg="white", border=0,
                                                                                  command=left_pin_c)
                                                    self.leftc_button.place(x=186, y=13)

                                                    self.buttonc1 = tk.Button(self.frame_otp, text="1",
                                                                              font=('Helvetica', 13, 'bold'), bg="#d9d9d9",
                                                                              border=0,activebackground="#d9d9d9",
                                                                              command=buttonc1)
                                                    self.buttonc1.place(x=47, y=97)

                                                    self.buttonc2 = tk.Button(self.frame_otp, text="2",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              bg="#d9d9d9",activebackground="#d9d9d9",
                                                                              command=buttonc2)
                                                    self.buttonc2.place(x=97, y=97)

                                                    self.buttonc3 = tk.Button(self.frame_otp, text="3",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              bg="#d9d9d9",activebackground="#d9d9d9",
                                                                              command=buttonc3)
                                                    self.buttonc3.place(x=147, y=95)

                                                    self.buttonc4 = tk.Button(self.frame_otp, text="4",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              command=buttonc4)
                                                    self.buttonc4.place(x=47, y=140)

                                                    self.buttonc5 = tk.Button(self.frame_otp, text="5",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              command=buttonc5)
                                                    self.buttonc5.place(x=97, y=140)

                                                    self.buttonc6 = tk.Button(self.frame_otp, text="6",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              command=buttonc6)
                                                    self.buttonc6.place(x=147, y=140)

                                                    self.buttonc7 = tk.Button(self.frame_otp, text="7",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              command=buttonc7)
                                                    self.buttonc7.place(x=47, y=185)

                                                    self.buttonc8 = tk.Button(self.frame_otp, text="8",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              command=buttonc8)
                                                    self.buttonc8.place(x=97, y=185)

                                                    self.buttonc9 = tk.Button(self.frame_otp, text="9",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              command=buttonc9)
                                                    self.buttonc9.place(x=147, y=185)

                                                    self.buttonc0 = tk.Button(self.frame_otp, text="0",
                                                                              font=('Helvetica', 13, 'bold'), border=0,
                                                                              command=buttonc0)
                                                    self.buttonc0.place(x=97, y=230)

                                                    self.button_hapusc = tk.Button(self.frame_otp, text="⬅",
                                                                                   font=('Helvetica', 16, 'bold'), border=0,
                                                                                   activebackground="#e4b672",
                                                                                   activeforeground="white", bg="#e4b672",
                                                                                   fg="white",
                                                                                   command=hapusc111)
                                                    self.button_hapusc.place(x=29, y=240)

                                                    self.button_submitc = tk.Button(self.frame_otp, text="✅",
                                                                                    font=('Helvetica', 16, 'bold'),
                                                                                    border=0,
                                                                                    bg="#FDCB7F", fg="white",
                                                                                    activebackground="#FDCB7F",
                                                                                    activeforeground="white",
                                                                                    command=submit_checkOTP
                                                                                    )
                                                    self.button_submitc.place(x=140, y=240)

                                                else:
                                                    self.frame_9 = tk.Frame(self.roots)
                                                    self.frame_9.place(x=520, y=270)

                                                    bg3_image = Image.open("images\Frame 63.png")
                                                    resize_image = bg3_image.resize((219, 227))
                                                    self.photo2 = ImageTk.PhotoImage(resize_image)

                                                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                                    self.lbl_frame.image = self.photo2
                                                    self.lbl_frame.pack()

                                                    def oouutt():
                                                        self.frame_9.destroy()

                                                    self.outbut9 = tk.Button(self.frame_9,
                                                                             font=('Helvetica'),
                                                                             text="x",
                                                                             fg="#ffffff",
                                                                             bg="#FDCB7F",
                                                                             border=0,
                                                                             activebackground="#FDCB7F",
                                                                             activeforeground="#ffffff",
                                                                             cursor="hand2",
                                                                             width=3,
                                                                             command=oouutt)
                                                    self.outbut9.place(x=175, y=7)

                                            self.leftcheck_button = tk.Button(self.frame_check, text="X",
                                                                              font=('Helvetica', 10, 'bold'),
                                                                              activebackground="#fdcb7f",
                                                                              activeforeground="white", bg="#fdcb7f",
                                                                              fg="white", border=0,
                                                                              command=left_pin_check)
                                            self.leftcheck_button.place(x=340, y=8)

                                            self.button_otp = tk.Button(self.frame_check, text="Lanjutkan",
                                                                        font=('Helvetica', 14, 'bold'), bg="#ffa41c",
                                                                        fg='black',
                                                                        border=0, width=10, activebackground="#ffa41c",
                                                                        activeforeground="black",
                                                                        command=otp_button)
                                            self.button_otp.place(x=120, y=78)
                                else:
                                    self.frame_9 = tk.Frame(self.roots)
                                    self.frame_9.place(x=520, y=270)

                                    bg3_image = Image.open("images\Frame 32.png")
                                    resize_image = bg3_image.resize((219, 227))
                                    self.photo2 = ImageTk.PhotoImage(resize_image)

                                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                    self.lbl_frame.image = self.photo2
                                    self.lbl_frame.pack()

                                    def oouutt():
                                        self.frame_9.destroy()

                                    self.outbut9 = tk.Button(self.frame_9,
                                                             font=('Helvetica'),
                                                             text="x",
                                                             fg="#ffffff",
                                                             bg="#FDCB7F",
                                                             border=0,
                                                             activebackground="#FDCB7F",
                                                             activeforeground="#ffffff",
                                                             cursor="hand2",
                                                             width=3,
                                                             command=oouutt)
                                    self.outbut9.place(x=175, y=7)
                            elif row_norek is not None:
                                self.frame_9 = tk.Frame(self.roots)
                                self.frame_9.place(x=520, y=270)

                                bg3_image = Image.open("images\Frame 56.png")
                                resize_image = bg3_image.resize((219, 227))
                                self.photo2 = ImageTk.PhotoImage(resize_image)

                                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                self.lbl_frame.image = self.photo2
                                self.lbl_frame.pack()

                                def oouutt():
                                    self.frame_9.destroy()

                                self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                                self.outbut9.place(x=175, y=7)

                            else:
                                self.frame_9 = tk.Frame(self.roots)
                                self.frame_9.place(x=520, y=270)

                                bg3_image = Image.open("images\Frame 31.png")
                                resize_image = bg3_image.resize((219, 227))
                                self.photo2 = ImageTk.PhotoImage(resize_image)

                                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                self.lbl_frame.image = self.photo2
                                self.lbl_frame.pack()

                                def oouutt():
                                    self.frame_9.destroy()

                                self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                                self.outbut9.place(x=175, y=7)
                        else:
                            self.frame_9 = tk.Frame(self.roots)
                            self.frame_9.place(x=520, y=270)

                            bg3_image = Image.open("images\Frame 29.png")
                            resize_image = bg3_image.resize((219, 227))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            def oouutt():
                                self.frame_9.destroy()

                            self.outbut9 = tk.Button(self.frame_9,
                                                     font=('Helvetica'),
                                                     text="x",
                                                     fg="#ffffff",
                                                     bg="#FDCB7F",
                                                     border=0,
                                                     activebackground="#FDCB7F",
                                                     activeforeground="#ffffff",
                                                     cursor="hand2",
                                                     width=3,
                                                     command=oouutt)
                            self.outbut9.place(x=175, y=7)
                    else:
                        self.frame_9 = tk.Frame(self.roots)
                        self.frame_9.place(x=520, y=270)

                        bg3_image = Image.open("images\Frame 28.png")
                        resize_image = bg3_image.resize((219, 227))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()

                        def oouutt():
                            self.frame_9.destroy()

                        self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                        self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.roots)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 27.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
            else:
                    self.frame_9 = tk.Frame(self.roots)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 68.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)

        def syarat_dan_ketentuan():
            def out_from_snk():
                self.frameSNK1.destroy()
            def page5():
                def page4():
                    def page3():
                        def page2():
                            def backTo1():
                                self.frameSNK2.destroy()
                            def next(): #ini jadi command previous
                                self.frameSNK2.destroy()

                            self.frameSNK2 = tk.Frame(self.roots)
                            self.frameSNK2.place(x=380,y=60)

                            bg3_image = Image.open("images\Frame 70 (1).png")
                            resize_image = bg3_image.resize((500, 600))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frameSNK2, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            self.next2 = tk.Button(self.frameSNK2,
                                                 font=('Helvetica',20),
                                                 text="▶️",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=backTo1)
                            self.next2.place(x=89, y=540)

                            self.back2 = tk.Button(self.frameSNK2,
                                                    font=('Helvetica',20),
                                                    text="◀️",
                                                    fg="#ffffff",
                                                    bg="#FDCB7F",
                                                    border=0,
                                                    activebackground="#FDCB7F",
                                                    activeforeground="#ffffff",
                                                    cursor="hand2",
                                                    width=3,
                                                    command=next)
                            self.back2.place(x=27, y=540)

                        def backTo4(): #ini jadi command next
                            self.frameSNK3.destroy()
                        self.frameSNK3 = tk.Frame(self.roots)
                        self.frameSNK3.place(x=380,y=60)
                        bg3_image = Image.open("images\Frame 73 (1).png")
                        resize_image = bg3_image.resize((500, 600))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frameSNK3, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()
                        self.frameSNK3 = tk.Frame(self.roots)
                        self.next3 = tk.Button(self.frameSNK3,
                                             font=('Helvetica',20),
                                             text="▶️",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=backTo4)
                        self.next3.place(x=89, y=540)

                        self.back3 = tk.Button(self.frameSNK3,
                                            font=('Helvetica',20),
                                            text="◀️",
                                            fg="#ffffff",
                                            bg="#FDCB7F",
                                            border=0,
                                            activebackground="#FDCB7F",
                                            activeforeground="#ffffff",
                                            cursor="hand2",
                                            width=3,
                                            command=page2)
                        self.back3.place(x=27, y=540)
                    def backTo5(): #ini jadi command next
                        self.frameSNK4.destroy()

                    self.frameSNK4 = tk.Frame(self.roots)
                    self.frameSNK4.place(x=380,y=60)

                    bg3_image = Image.open("images\Frame 72 (1).png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frameSNK4, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    self.next4 = tk.Button(self.frameSNK4,
                                         font=('Helvetica',20),
                                         text="▶️",
                                         fg="#ffffff",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="#ffffff",
                                         cursor="hand2",
                                         width=3,
                                         command=backTo5)
                    self.next4.place(x=89, y=540)

                    self.back4 = tk.Button(self.frameSNK4,
                                        font=('Helvetica',20),
                                        text="◀️",
                                        fg="#ffffff",
                                        bg="#FDCB7F",
                                        border=0,
                                        activebackground="#FDCB7F",
                                        activeforeground="#ffffff",
                                        cursor="hand2",
                                        width=3,
                                        command=page3)
                    self.back4.place(x=27, y=540)

                def out_from_snk(): #ini jadi command kembali
                    self.frameSNK1.destroy()

                self.frameSNK5 = tk.Frame(self.roots)
                self.frameSNK5.place(x=380,y=60)

                bg3_image = Image.open("images\Frame 71 (1).png")
                resize_image = bg3_image.resize((500, 600))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frameSNK5, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()
                self.back5 = tk.Button(self.frameSNK5,
                                        font=('Helvetica',20),
                                        text="◀️",
                                        fg="#ffffff",
                                        bg="#FDCB7F",
                                        border=0,
                                        activebackground="#FDCB7F",
                                        activeforeground="#ffffff",
                                        cursor="hand2",
                                        width=3,
                                        command=page4)
                self.back5.place(x=27, y=540)

            def page2():
                def page3():
                    def page4():
                        def page5():
                            def backTo4(): #ini jadi command previous
                                self.frameSNKnext5.destroy()

                            self.frameSNKnext5 = tk.Frame(self.roots)
                            self.frameSNKnext5.place(x=380,y=60)

                            bg3_image = Image.open("images\Frame 71 (1).png")
                            resize_image = bg3_image.resize((500, 600))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frameSNKnext5, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            self.back5 = tk.Button(self.frameSNKnext5,
                                                font=('Helvetica',20),
                                                text="◀️",
                                                fg="#ffffff",
                                                bg="#FDCB7F",
                                                border=0,
                                                activebackground="#FDCB7F",
                                                activeforeground="#ffffff",
                                                cursor="hand2",
                                                width=3,
                                                command=backTo4)
                            self.back5.place(x=27, y=540)
                        def backTo3(): #ini jadi command previous
                            self.frameSNKnext4.destroy()

                        self.frameSNKnext4 = tk.Frame(self.roots)
                        self.frameSNKnext4.place(x=380,y=60)

                        bg3_image = Image.open("images\Frame 72 (1).png")
                        resize_image = bg3_image.resize((500, 600))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frameSNKnext4, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()

                        self.next4 = tk.Button(self.frameSNKnext4,
                                             font=('Helvetica',20),
                                             text="▶️",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=page5)
                        self.next4.place(x=89, y=540)

                        self.back4 = tk.Button(self.frameSNKnext4,
                                                font=('Helvetica',20),
                                                text="◀️",
                                                fg="#ffffff",
                                                bg="#FDCB7F",
                                                border=0,
                                                activebackground="#FDCB7F",
                                                activeforeground="#ffffff",
                                                cursor="hand2",
                                                width=3,
                                                command=backTo3)
                        self.back4.place(x=27, y=540)

                    def backTo2(): #ini jadi command previous
                        self.frameSNKnext3.destroy()

                    self.frameSNKnext3 = tk.Frame(self.roots)
                    self.frameSNKnext3.place(x=380,y=60)

                    bg3_image = Image.open("images\Frame 73 (1).png")
                    resize_image = bg3_image.resize((500, 600))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frameSNKnext3, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    self.next3 = tk.Button(self.frameSNKnext3,
                                         font=('Helvetica',20),
                                         text="▶️",
                                         fg="#ffffff",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="#ffffff",
                                         cursor="hand2",
                                         width=3,
                                         command=page4)
                    self.next3.place(x=89, y=540)

                    self.back3 = tk.Button(self.frameSNKnext3,
                                        font=('Helvetica',20),
                                        text="◀️",
                                        fg="#ffffff",
                                        bg="#FDCB7F",
                                        border=0,
                                        activebackground="#FDCB7F",
                                        activeforeground="#ffffff",
                                        cursor="hand2",
                                        width=3,
                                        command=backTo2)
                    self.back3.place(x=27, y=540)

                   
                def backTo1(): #ini jadi command previous
                    self.frameSNKnext2.destroy()

                self.frameSNKnext2 = tk.Frame(self.roots)
                self.frameSNKnext2.place(x=380,y=60)

                bg3_image = Image.open("images\Frame 70 (1).png")
                resize_image = bg3_image.resize((500, 600))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frameSNKnext2, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                self.next2 = tk.Button(self.frameSNKnext2,
                                     font=('Helvetica',20),
                                     text="▶️",
                                     fg="#ffffff",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="#ffffff",
                                     cursor="hand2",
                                     width=3,
                                     command=page3)
                self.next2.place(x=89, y=540)

                self.back2 = tk.Button(self.frameSNKnext2,
                                    font=('Helvetica',20),
                                    text="◀️",
                                    fg="#ffffff",
                                    bg="#FDCB7F",
                                    border=0,
                                    activebackground="#FDCB7F",
                                    activeforeground="#ffffff",
                                    cursor="hand2",
                                    width=3,
                                    command=backTo1)
                self.back2.place(x=27, y=540)


            self.frameSNK1 = tk.Frame(self.roots)
            self.frameSNK1.place(x=380,y=60)

            bg3_image = Image.open("images\Frame 69 (5).png")
            resize_image = bg3_image.resize((500, 600))
            self.photo2 = ImageTk.PhotoImage(resize_image)

            self.lbl_frame = tk.Label(self.frameSNK1, image=self.photo2)
            self.lbl_frame.image = self.photo2
            self.lbl_frame.pack()

            self.next1 = tk.Button(self.frameSNK1,
                                 font=('Helvetica',20),
                                 text="▶️",
                                 fg="#ffffff",
                                 bg="#FDCB7F",
                                 border=0,
                                 activebackground="#FDCB7F",
                                 activeforeground="#ffffff",
                                 cursor="hand2",
                                 width=3,
                                 command=page2)
            self.next1.place(x=27, y=540)

            self.kembali1 = tk.Button(self.frameSNK1,
                                     font=('Helvetica',18),
                                     text="Kembali",
                                     fg="#ffffff",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="#ffffff",
                                     cursor="hand2",
                                     width=8,
                                     command=out_from_snk)
            self.kembali1.place(x=350, y=545)
                
        def out_from_signupMenu():
            self.roots.destroy()
            self.bsd.deiconify()

        def username_textt(y):
            user = self.username_create.get()
            if user =="Username":
                self.username_create.delete(0, "end")

        def zoomout(e):
            name = self.username_create.get()
            if name == "":
                self.username_create.insert(0,"Username")

        def email_textt(e):
            emaill = self.email_create.get()
            if emaill == "Email":
                self.email_create.delete(0,"end")

        def email_zoomout(e):
            mail = self.email_create.get()
            if mail == "":
                self.email_create.insert(0,"Email")
        #
        def password_textt(e):
            passw = self.password_create.get()
            if passw == "Password":
                self.password_create.delete(0,"end")

        def password_zoomout(e):
            names = self.password_create.get()
            if names == "":
                self.password_create.insert(0,"Password")
        #
        def pin_text(e):
            pin = self.pin_create.get()
            if pin == "PIN":
                self.pin_create.delete(0,"end")
        #
        def pin_zoomout(e):
            name = self.pin_create.get()
            if name == "":
                self.pin_create.insert(0,"PIN")
        #
        def norek_text(e):
            nim = self.norek_create.get()
            if nim == "NIM":
                self.norek_create.delete(0,"end")
        #
        def norek_zoomout(e):
            name = self.norek_create.get()
            if name == "":
                self.norek_create.insert(0,"NIM")
        #
        def depo_text(e):
            name = self.depo_create.get()
            if name == "Deposit Min. 150000":
                self.depo_create.delete(0,"end")
        #
        def depo_zoomout(e):
            name = self.depo_create.get()
            if name == "":
                self.depo_create.insert(0,"Deposit Min. 150000")
                
        self.username_create = tk.Entry(self.roots,
                                        font=('Helvetica', 18),
                                        fg="black",
                                        bg="#ffffff",
                                        border=0,
                                        width=17)
        self.username_create.place(x=490, y=170)
        self.username_create.insert(0, "Username")
        self.username_create.bind('<FocusIn>', username_textt)
        self.username_create.bind('<FocusOut>', zoomout)

        self.password_create = tk.Entry(self.roots,
                                        font=('Helvetica', 18),
                                        fg="black",
                                        bg="#ffffff",
                                        border=0,
                                        width=17)
        self.password_create.place(x=490, y=225)
        self.password_create.insert(0, "Password")
        self.password_create.bind('<FocusIn>', password_textt)
        self.password_create.bind('<FocusOut>', password_zoomout)

        self.pin_create = tk.Entry(self.roots,
                                   font=('Helvetica', 18),
                                   fg="black",
                                   bg="#ffffff",
                                   border=0,
                                   width=17)
        self.pin_create.place(x=490, y=275)
        self.pin_create.insert(0, "PIN")
        self.pin_create.bind('<FocusIn>', pin_text)
        self.pin_create.bind('<FocusOut>', pin_zoomout)

        self.norek_create = tk.Entry(self.roots,
                                     font=('Helvetica', 18),
                                     fg="black",
                                     bg="#ffffff",
                                     width=17,
                                     border=0)
        self.norek_create.place(x=490, y=325)
        self.norek_create.insert(0, "NIM")
        self.norek_create.bind('<FocusIn>', norek_text)
        self.norek_create.bind('<FocusOut>', norek_zoomout)

        self.depo_create = tk.Entry(self.roots,
                                    font=('Helvetica', 18),
                                    fg="black",
                                    bg="#ffffff",
                                    width=17,
                                    border=0)
        self.depo_create.place(x=490, y=375)
        self.depo_create.insert(0, "Deposit Min. 150000")
        self.depo_create.bind('<FocusIn>', depo_text)
        self.depo_create.bind('<FocusOut>', depo_zoomout)

        self.email_create = tk.Entry(self.roots,
                                   font=('Helvetica', 18),
                                   fg="black",
                                   bg="#ffffff",
                                   border=0,
                                   width=17)
        self.email_create.place(x=490, y=425)
        self.email_create.insert(0, "Email")
        self.email_create.bind('<FocusIn>', email_textt)
        self.email_create.bind('<FocusOut>', email_zoomout)

        self.signup_button = tk.Button(self.roots,
                                       text='Daftar',
                                       font=("Helvetica", 18),
                                       command=signup_button,
                                       fg="black",
                                       bg="#FDCB7F",
                                       width=23,
                                       border=0,
                                       activebackground="#FDCB7F",
                                       activeforeground="#ffffff",
                                       cursor="hand2")
        self.signup_button.place(x=470, y=518)

        self.outbutt = tk.Button(self.roots,
                                text='Kembali',
                                font=("Helvetica", 18),
                                command=out_from_signupMenu,
                                 fg="black",
                                 bg="#FDCB7F",
                                 width=23,
                                 border=0,
                                 activebackground="#FDCB7F",
                                 activeforeground="#ffffff",
                                 cursor="hand2")
        self.outbutt.place(x=470, y=572)

        self.skbutt = tk.Button(self.roots,
                                text='Syarat & Ketentuan📝',
                                font=("Helvetica", 10),
                                command=syarat_dan_ketentuan,
                                 fg="black",
                                 bg="#FDCB7F",
                                 width=19,
                                 border=0,
                                 activebackground="#FDCB7F",
                                 activeforeground="black",
                                 cursor="hand2")
        self.skbutt.place(x=611, y=470)
        
        checkbox_var = tk.BooleanVar()
        centang_checkbox = tk.Checkbutton(self.roots, activebackground="white",bg="white",border=0,variable=checkbox_var)
        centang_checkbox.place(x=780, y=475)
        

        self.roots.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.hashingFunction(self.password_entry.get())

        row = self.data_user.find_one({'username':username, 'password':password})

        if row is not None and username!="Username" and password!="Password" and username!="" and password!="":
            self.balance = row.get('balance')
            self.balance = int(self.balance)
            self.login_username = username
            self.Main_frame()
            self.name = row.get('username')
            myrek = row.get('nomor_rekening')
            self.myRekening = myrek

        elif username == "Username" and password == "Password" and username!="" and password!="":
            self.frame_9 = tk.Frame(self.bsd)
            self.frame_9.place(x=520, y=270)

            bg3_image = Image.open("images\Frame 33.png")
            resize_image = bg3_image.resize((219, 227))
            self.photo2 = ImageTk.PhotoImage(resize_image)

            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
            self.lbl_frame.image = self.photo2
            self.lbl_frame.pack()

            def oouutt():
                self.frame_9.destroy()

            self.outbut9 = tk.Button(self.frame_9,
                                     font=('Helvetica'),
                                     text="x",
                                     fg="#ffffff",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="#ffffff",
                                     cursor="hand2",
                                     width=3,
                                     command=oouutt)
            self.outbut9.place(x=175, y=7)

        else:
            self.frame_9 = tk.Frame(self.bsd)
            self.frame_9.place(x=520, y=270)

            bg3_image = Image.open("images\Frame 35.png")
            resize_image = bg3_image.resize((219, 227))
            self.photo2 = ImageTk.PhotoImage(resize_image)

            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
            self.lbl_frame.image = self.photo2
            self.lbl_frame.pack()

            def oouutt():
                self.frame_9.destroy()

            self.outbut9 = tk.Button(self.frame_9,
                                     font=('Helvetica'),
                                     text="x",
                                     fg="#ffffff",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="#ffffff",
                                     cursor="hand2",
                                     width=3,
                                     command=oouutt)
            self.outbut9.place(x=175, y=7)

    def Main_frame(self):
        self.mains = Toplevel(self.bsd)
        self.mains.geometry('1280x720')
        self.mains.attributes('-fullscreen', True)
        bg3_image = Image.open("images\Frame 24 (4).png")  #Firdaini Azmi (23031554071)
        resize_imge = bg3_image.resize((1280, 720))
        photo2 = ImageTk.PhotoImage(resize_imge)
        self.lbl2 = tk.Label(self.mains, image=photo2)
        self.lbl2.place(x=0, y=0)
        self.mains.configure(bg="black")

        def quitbuttonM():
            self.frame_logout = tk.Frame(self.mains)
            self.frame_logout.place(x=440, y=270)

            bg3_image = Image.open("images\Frame 51.png")
            resize_image = bg3_image.resize((520, 187))
            self.photo2 = ImageTk.PhotoImage(resize_image)

            self.lbl_frame = tk.Label(self.frame_logout, image=self.photo2)
            self.lbl_frame.image = self.photo2
            self.lbl_frame.pack()

            def outMF():
                self.frame_logout.destroy()
                self.mains.destroy()
                self.mains.quit()
                self.password_entry.delete(0, 'end')
                self.username_entry.delete(0, 'end')
            def stayMF():
                self.frame_logout.destroy()

            self.yesbutt = tk.Button(self.frame_logout,
                                     font=('Helvetica',18,'bold'),
                                     text="Iya",
                                     fg="black",
                                     bg="#ffa41c",
                                     border=0,
                                     activebackground="#ffa41c",
                                     activeforeground="black",
                                     cursor="hand2",
                                     width=10,
                                     command=outMF)
            self.yesbutt.place(x=297, y=105)
            self.nobutt = tk.Button(self.frame_logout,
                                     font=('Helvetica',18,'bold'),
                                     text="Tidak",
                                     fg="black",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="black",
                                     cursor="hand2",
                                     width=10,
                                     command=stayMF)
            self.nobutt.place(x=75, y=105)

        def norekTujuan(e):
            nim = self.norek_tujuan.get()
            if nim == "No. Rek Tujuan":
                self.norek_tujuan.delete(0,"end")
        #
        def norekTujuan_zoomout(e):
            name = self.norek_tujuan.get()
            if name == "":
                self.norek_tujuan.insert(0,"No. Rek Tujuan")
        #
        def nom_tf(e):
            nim = self.nominalTF.get()
            if nim == "Nominal":
                self.nominalTF.delete(0,"end")
        #
        def nomTf_zoomout(e):
            name = self.nominalTF.get()
            if name == "":
                self.nominalTF.insert(0,"Nominal")

        self.norek_tujuan = tk.Entry(self.mains,
                                     font=('Helvetica', 20),
                                     fg="#777777",
                                     bg="white",
                                     width=19,
                                     border=0
                                     )
        self.norek_tujuan.place(x=535, y=152)
        self.norek_tujuan.insert(0, "No. Rek Tujuan")
        self.norek_tujuan.bind('<FocusIn>', norekTujuan)
        self.norek_tujuan.bind('<FocusOut>', norekTujuan_zoomout)
        self.no_reke = self.norek_tujuan.get()

        self.nominalTF = tk.Entry(self.mains,
                                     font=('Helvetica', 20),
                                     fg="#777777",
                                     bg="white",
                                     width=19,
                                     border=0,
                                     )
        self.nominalTF.place(x=540, y=212)
        self.nominalTF.insert(0, "Nominal")
        self.nominalTF.bind('<FocusIn>', nom_tf)
        self.nominalTF.bind('<FocusOut>', nomTf_zoomout)
        self.nominal_tf = self.nominalTF.get()

        self.transfer_button = tk.Button(self.mains,
                                         text='TRANSFER',
                                         command=self.newTransfer,
                                         font=("Helvetica", 15, 'bold'),
                                         fg="white",
                                         bg="#fdcb7f",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="white",
                                         cursor="hand2",
                                         width=25,
                                         )
        self.transfer_button.place(x=540, y=278)

        self.info=tk.Button(self.mains,         #Firdaini Azmi (23031554071)
                                     font=('Helvetica',12,'bold'),
                                     text="i",
                                     fg="white",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="white",
                                     cursor="hand2",
                                     width=2,
                                     anchor='center',
                                     command=self.infotf)
        self.info.place(x=830, y=105)


        self.withdraw_button = tk.Button(self.mains,
                                          text='WITHDRAW',
                                          command=self.withdraww,
                                         font=("Helvetica", 20,'bold'),
                                         fg="white",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="white",
                                         cursor="hand2",
                                         width=14,
                                          )
        self.withdraw_button.place(x=212, y=480)
        #
        self.e_commerce = tk.Button(self.mains,
                                    text='E-Commerce',
                                    font=("Helvetica", 20,'bold'),
                                    fg="white",
                                    bg="#FDCB7F",
                                    border=0,
                                    activebackground="#FDCB7F",
                                    activeforeground="white",
                                    cursor="hand2",
                                    width=14,
                                    command=self.Ecommerce
                                    )
        self.e_commerce.place(x=212, y=588)
        #
        self.deposit_button = tk.Button(self.mains,
                                         text='DEPOSIT',
                                         command=self.depo,
                                        font=("Helvetica",20,'bold'),
                                        fg="white",
                                        bg="#FDCB7F",
                                        border=0,
                                        activebackground="#FDCB7F",
                                        activeforeground="white",
                                        cursor="hand2",
                                        width=14,)
        self.deposit_button.place(x=212, y=380)

        image_path = "images\Frame 55 (1).png"  
        img = Image.open(image_path)
        resize_img = img.resize((90,90))
        self.button_image_withdraw2 = ImageTk.PhotoImage(resize_img)
        self.withdraw2_button = tk.Button(self.mains,
                                         command=self.withdraww,
                                         cursor="hand2",
                                         image = self.button_image_withdraw2,
                                         border=0)
        self.withdraw2_button.place(x=1055, y=247)

        image_path = "images\Frame 54 (1).png"  
        img = Image.open(image_path)
        resize_img = img.resize((90,90))
        self.button_image_deposit2 = ImageTk.PhotoImage(resize_img)
        self.deposit2_button = tk.Button(self.mains,
                                         command=self.depo,
                                         cursor="hand2",
                                         image = self.button_image_deposit2,
                                          border=0)
        self.deposit2_button.place(x=946, y=247)
        
        img = Image.open("images\Frame 53 (1).png")
        resize_img = img.resize((90,90))
        self.button_image_e_commerce2 = ImageTk.PhotoImage(resize_img)
        self.e_commerce2_button = tk.Button(self.mains,
                                         command=self.Ecommerce,
                                         cursor="hand2",
                                         image = self.button_image_e_commerce2,
                                         border=0)
        self.e_commerce2_button.place(x=1169, y=247)
        
        self.quit_button = tk.Button(self.mains,
                                 text='LOGOUT',
                                 font=("Helvetica", 15),
                                 command=quitbuttonM,
                                 fg="#ffffff",
                                 bg="#E4B672",
                                 border=0,
                                 activebackground="#E4B672",
                                 activeforeground="#ffffff",
                                 cursor="hand2",
                                      width=11)
        self.quit_button.place(x=1140, y=13)

        self.show_and_hide_balance_button = tk.Button(self.mains,
                                                      text='👁',
                                                      command=self.toggle_command,
                                                      border=0,
                                                      font=('Helvetica', 15),
                                                      bg='white',
                                                      fg="#FDCB7F"
                                                      )
        self.show_and_hide_balance_button.place(x=422, y=146)

        self.hide_balance_label1 = tk.Label(self.mains,
                                           text='● ● ● ● ●',
                                           font=('Helvetica', 22),
                                           bg='white',
                                           fg="black",
                                            width=14,
                                            anchor="w")
        self.hide_balance_label1.place(x=183, y=146)



        userSplit = self.login_username
        self.greeting_label = tk.Label(self.mains,
                                       font=('Encode Sans Semi Condensed', 22, 'bold'),
                                       bg='white',
                                       width=18,
                                       text=f"Welcome, {userSplit.split()[0]}")
        self.greeting_label.place(x=935, y=87)

        self.time_label = tk.Label(self.mains,
                                   font=('Helvetica', 45, 'bold'),
                                   bg='white',
                                   width=9)
        self.time_label.place(x=935, y=120)

        self.date_label = tk.Label(self.mains,
                                   font=('Helvetica', 20,'bold'),
                                   bg='white',
                                   width=18)
        self.date_label.place(x=955, y=198)

        self.update_time()
        username = self.username_entry.get()
        password = self.hashingFunction(self.password_entry.get())
        row = self.data_user.find_one({'username':username, 'password':password})
        myReke = row.get('nomor_rekening')
        myReke = int(myReke)
        myCard = row.get('nomor_kartu')
        myCard = myCard

        self.norek_label = tk.Label(self.mains,
                                    font=('Helvetica', 14, 'bold'),
                                    bg='white',
                                    fg="black",
                                    width=18,
                                    anchor='w',
                                    text=f"{myReke}")
        self.norek_label.place(x=515, y=667)

        self.norek_label = tk.Label(self.mains,
                                    font=('Helvetica', 14, 'bold'),
                                    bg='#77878c',
                                    border=0,
                                    fg="white",
                                    text=f"{myCard}")
        self.norek_label.place(x=510, y=565)

        self.frame_h = tk.Frame(self.mains)
        self.frame_h.place(x=932, y=387)

        self.my_canvas = tk.Canvas(self.frame_h, width=320, height=320, bg="white")
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        self.scrollbar = ttk.Scrollbar(self.frame_h, orient=VERTICAL, command=self.my_canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.my_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.my_canvas.bind("<Configure>", lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))

        self.loadHistory(self.login_username)

        self.mains.mainloop()

    def loadHistory(self, username):

        rows = self.transaction_history.find({"username":username}).sort([("_id", pymongo.ASCENDING)])

        for row in rows:
            transaction_type = row.get('transaction_type')
            nominal = row.get('nominal_transaction')
            timestamps = row.get('time_transaction')
            try:
                locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                nominal_lokal = locale.format_string("%d", nominal, grouping=True)

                if transaction_type == "Deposit" or "Transfer ":
                    Nominal_format = f"+{nominal_lokal}"
                else:
                    Nominal_format = f"-{nominal_lokal}"

            finally:
                frame_loadH = tk.LabelFrame(self.my_canvas)

                bg3_image = Image.open("images\Frame 42.png")
                resize_image = bg3_image.resize((320, 80))
                photo2 = ImageTk.PhotoImage(resize_image)

                lbl_frame = tk.Label(frame_loadH, image=photo2)
                lbl_frame.image = photo2
                lbl_frame.pack()

                transaction_type_label = tk.Label(frame_loadH,
                                              text=f'{transaction_type}',
                                              font=('Comic Sans', 17),
                                              bg="#F6C57B",
                                              border=0,
                                              width=10,
                                              anchor='w')
                transaction_type_label.place(x=2, y=2)

                date_transaction_label = tk.Label(frame_loadH,
                                              text=f"{timestamps}",
                                              font=('Comic Sans', 10), bg="#E4B672",
                                              border=0, width=15)
                date_transaction_label.place(x=200, y=60)

                nominal_transaction_label = tk.Label(frame_loadH,
                                                 text=f'{Nominal_format}',
                                                 font=('Comic Sans', 20),
                                                 bg="#F6C57B",
                                                 anchor='e',
                                                 border=0,
                                                 width=12)
                nominal_transaction_label.place(x=130, y=2)

                y_position = len(self.my_canvas.winfo_children()) * 80
                self.my_canvas.create_window((0, y_position), window=frame_loadH, anchor="nw")
                self.my_canvas.update_idletasks()
                self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

    def create_history(self, transaction_type, nominal):
        try:
            timestamp = datetime.datetime.now()
            formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            usernameMutasi = self.login_username

            self.transaction_history.insert_one({
                '_id': ObjectId(),
                "username": usernameMutasi,
                "transaction_type": transaction_type,
                "nominal_transaction": nominal,
                "time_transaction": formatted_timestamp
            })

            locale.setlocale(locale.LC_NUMERIC, 'id_ID')
            nominal_lokal = locale.format_string("%d", nominal, grouping=True)

            if transaction_type == "Deposit":
                Nominal_format = f"+{nominal_lokal}"
            else:
                Nominal_format = f"-{nominal_lokal}"

        finally:
            self.frame_CH = tk.Frame(self.my_canvas)
            self.frame_CH.pack()

            bg3_image = Image.open("images\Frame 42.png")
            resize_image = bg3_image.resize((320, 80))
            self.photo2 = ImageTk.PhotoImage(resize_image)

            self.lbl_frame = tk.Label(self.frame_CH, image=self.photo2)
            self.lbl_frame.image = self.photo2
            self.lbl_frame.pack()

            transaction_type_label = tk.Label(self.frame_CH,
                                              text=f'{transaction_type}',
                                              font=('Comic Sans', 17),
                                              bg="#F6C57B",
                                              border=0,
                                              width=10,
                                              anchor='w')
            transaction_type_label.place(x=2, y=2)

            date_transaction_label = tk.Label(self.frame_CH,
                                              text=f"{formatted_timestamp}",
                                              font=('Comic Sans', 10), bg="#E4B672",
                                              border=0, width=15)
            date_transaction_label.place(x=200, y=60)

            nominal_transaction_label = tk.Label(self.frame_CH,
                                                 text=f'{Nominal_format}',
                                                 font=('Comic Sans', 20),
                                                 bg="#F6C57B",
                                                 anchor='e',
                                                 border=0,
                                                 width=12)
            nominal_transaction_label.place(x=130, y=2)

            y_position = len(self.my_canvas.winfo_children()) * 80
            self.my_canvas.create_window((0, y_position), window=self.frame_CH, anchor="nw")
            self.my_canvas.update_idletasks()
            self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        current_date = time.strftime('%d-%m-%Y')
        current_day = time.strftime('%A')

        self.time_label['text'] = current_time
        self.date_label['text'] = f'    {current_day}, {current_date}     '
        self.mains.after(1000, self.update_time)

    def infotf(self):   #Firdaini Azmi (23031554071)
        self.infotf = tk.Frame(self.mains)
        self.infotf.place(x=495,y=80)
        
        bg3_image = Image.open("images\Frame 78.png")
        resize_image = bg3_image.resize((379, 257))
        self.photo2 = ImageTk.PhotoImage(resize_image)

        self.lbl_frame = tk.Label(self.infotf, image=self.photo2)
        self.lbl_frame.image = self.photo2
        self.lbl_frame.pack()

        def oouutt():
            self.infotf.destroy()

        self.outbut9 = tk.Button(self.infotf,
                                             font=('Helvetica',18,'bold'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
        self.outbut9.place(x=330,y=3)
        
    def newTransfer(self):
        def submit_pin_tf():
            PIN_tf1 = self.pin_entry.get()
            norek = self.norek_tujuan.get()
            nominal = self.nominalTF.get()
            locale.setlocale(locale.LC_NUMERIC, 'id_ID')
            angka_terformat = locale.format_string('%d', int(nominal), grouping=True)

            random_number = random.randint(10000000,99999999)
            curent_time = time.strftime('%H:%M:%S')
            curent_date = time.strftime('%d-%m-%y')

            username = self.username_entry.get()
            password = self.hashingFunction(self.password_entry.get())
            no_resiTF = f'TF-{random_number}'

            row = self.data_user.find_one({'username':username,"password":password})
            myReke = row.get("nomor_rekening")
            myReke = int(myReke)

            self.frame_tf.destroy()

            row_pin = self.data_user.find_one({'pin':PIN_tf1, 'username':username,'password':password})

            if row_pin is not None and PIN_tf1 is not None:
                self.balance -= int(nominal)
                self.data_user.update_one(
                    {"nomor_rekening": norek},
                    {"$inc": {"balance": int(nominal)}}
                )

                self.data_user.update_one(
                    {"username": self.login_username},
                    {"$set": {"balance": int(self.balance)}}
                )

                if self.click_count % 2 == 1:
                    self.show_balance()
                else:
                    pass

                self.create_history("Transfer", int(nominal))

                mutasii = self.data_user.find_one({"nomor_rekening":norek})
                usernameTujuann = mutasii.get('username')
                typeTransaction = "Transfer "
                timestamp = datetime.datetime.now()
                formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                self.transaction_history.insert_one({
                    '_id': ObjectId(),
                    "username": usernameTujuann,
                    "transaction_type": typeTransaction,
                    "nominal_transaction": nominal,
                    "time_transaction": formatted_timestamp
                })

                self.print_receipt(f'Transfer to {norek}',
                                   angka_terformat,
                                   no_resiTF)

                def left_transaksi():
                    self.frame_transaksi_t.destroy()

                self.frame_transaksi_t = tk.Frame(self.mains)
                self.frame_transaksi_t.place(x=550, y=250)

                bg3_image = Image.open("images\Frame 10.png")
                resize_image = bg3_image.resize((211, 293))
                self.photo2 = ImageTk.PhotoImage(resize_image)
                

                self.lbt_frame = tk.Label(self.frame_transaksi_t, image=self.photo2)
                self.lbt_frame.image = self.photo2
                self.lbt_frame.pack()
                    
                self.left = tk.Button(self.frame_transaksi_t, text="X", font=('Helvetica', 10, 'bold'), bg="#e4b672",
                                                  fg="white",
                                        border=0, command=left_transaksi)
                self.left.place(x=180, y=9)

                self.name = tk.Label(self.frame_transaksi_t, text=f'{self.login_username}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                     bg="#fdcb7f")
                self.name.place(x=80, y=75)

                self.no_rek = tk.Label(self.frame_transaksi_t, text=f'{myReke}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                      bg="#fdcb7f")
                self.no_rek.place(x=80, y=97)
                
                self.tujuan = tk.Label(self.frame_transaksi_t, text=f'TF To {norek}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                      bg="#fdcb7f")
                self.tujuan.place(x=80, y=119)

                self.nominal = tk.Label(self.frame_transaksi_t, text=f'{angka_terformat}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                      bg="#fdcb7f")
                self.nominal.place(x=80, y=139)

                self.tanggal = tk.Label(self.frame_transaksi_t, text=f'{curent_time}, {curent_date}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                      bg="#fdcb7f")
                self.tanggal.place(x=80, y=160)

                self.no_resi = tk.Label(self.frame_transaksi_t, text=no_resiTF,width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                      bg="#fdcb7f")
                self.no_resi.place(x=80, y=183)

                self.norek_tujuan.delete(0, "end")
                self.nominalTF.delete(0, "end")
                self.norek_tujuan.insert(0, "No. Rek Tujuan")
                self.nominalTF.insert(0, "Nominal")

            elif len(str(PIN_tf1)) != 6:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 29.png")
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                         font=('Helvetica'),
                                         text="x",
                                         fg="#ffffff",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="#ffffff",
                                         cursor="hand2",
                                         width=3,
                                         command=oouutt)
                self.outbut9.place(x=175, y=7)
            else:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 34.png")
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                         font=('Helvetica'),
                                         text="x",
                                         fg="#ffffff",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="#ffffff",
                                         cursor="hand2",
                                         width=3,
                                         command=oouutt)
                self.outbut9.place(x=175, y=7)

        norek = self.norek_tujuan.get()
        nominalTF = self.nominalTF.get()
        username = self.username_entry.get()
        password = self.hashingFunction(self.password_entry.get())

        row = self.data_user.find_one({"username":username, "password":password})

        myReke = row.get('nomor_rekening')

        row5 = self.data_user.find_one({'nomor_rekening':norek})

        if row5 is not None and norek!=myReke:
            if str(nominalTF).isdigit():
                if self.balance - int(nominalTF)>= 20000:
                    if self.balance >= int(nominalTF):
                        if int(nominalTF) >= 10000:
                            locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                            angka_terformat = locale.format_string('%d', int(nominalTF), grouping=True)

                            self.frame_konfirmasi = tk.Frame(self.mains)
                            self.frame_konfirmasi.place(x=420, y=200)

                            bg3_image = Image.open("images\Frame 47 (2).png")
                            resize_image = bg3_image.resize((520, 302))
                            self.photo2 = ImageTk.PhotoImage(resize_image)
                            

                            self.lbk_frame = tk.Label(self.frame_konfirmasi, image=self.photo2)
                            self.lbk_frame.image = self.photo2
                            self.lbk_frame.pack()

                            def left_transaksi():
                                self.frame_konfirmasi.destroy()
                            def batal_transaksi():
                                self.frame_konfirmasi.destroy()
                            def next_transaksi():
                                self.frame_konfirmasi.destroy()
                                self.frame_tf = tk.Frame(self.mains)
                                self.frame_tf.place(x=590, y=270)

                                def button1():
                                    self.pin_entry.insert(tk.END, 1)

                                def button2():
                                    self.pin_entry.insert(tk.END, 2)

                                def button3():
                                    self.pin_entry.insert(tk.END, 3)

                                def button4():
                                    self.pin_entry.insert(tk.END, 4)

                                def button5():
                                    self.pin_entry.insert(tk.END, 5)

                                def button6():
                                    self.pin_entry.insert(tk.END, 6)

                                def button7():
                                    self.pin_entry.insert(tk.END, 7)

                                def button8():
                                    self.pin_entry.insert(tk.END, 8)

                                def button9():
                                    self.pin_entry.insert(tk.END, 9)

                                def button00():
                                    self.pin_entry.insert(tk.END, 0)

                                def button0():
                                    self.pin_entry.insert(tk.END, 0)

                                def button0():
                                    self.pin_entry.insert(tk.END, 0)

                                def hapus111():
                                    self.pin_entry.delete(0, tk.END)

                                def left_pin_tf():
                                    self.frame_tf.destroy()


                                bg3_image = Image.open("images\Frame 9.png")
                                resize_image = bg3_image.resize((211, 293))
                                self.photo2 = ImageTk.PhotoImage(resize_image)

                                self.lbl_frame = tk.Label(self.frame_tf, image=self.photo2)
                                self.lbl_frame.image = self.photo2
                                self.lbl_frame.pack()

                                self.pin_entry = tk.Entry(self.frame_tf, font=('Helvetica', 16, 'bold'), width=6, border=0,
                                                          bg="#d9d9d9")
                                self.pin_entry.place(x=68, y=52)

                                self.left_button= tk.Button(self.frame_tf, text="X", font=('Helvetica', 10, 'bold'),activebackground="#e4b672",
                                                     activeforeground="white", bg="#e4b672", fg="white",border=0,
                                         command=left_pin_tf)
                                self.left_button.place(x=186, y=13)

                                self.button1 = tk.Button(self.frame_tf, text="1", font=('Helvetica', 13, 'bold'), bg="#d9d9d9",
                                                         border=0,
                                                         command=button1)
                                self.button1.place(x=47, y=97)

                                self.button2 = tk.Button(self.frame_tf, text="2", font=('Helvetica', 13, 'bold'), border=0,
                                                         bg="#d9d9d9",
                                                         command=button2)
                                self.button2.place(x=97, y=97)

                                self.button3 = tk.Button(self.frame_tf, text="3", font=('Helvetica', 13, 'bold'), border=0,
                                                         bg="#d9d9d9",
                                                         command=button3)
                                self.button3.place(x=147, y=95)

                                self.button4 = tk.Button(self.frame_tf, text="4", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button4)
                                self.button4.place(x=47, y=140)

                                self.button5 = tk.Button(self.frame_tf, text="5", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button5)
                                self.button5.place(x=97, y=140)

                                self.button6 = tk.Button(self.frame_tf, text="6", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button6)
                                self.button6.place(x=147, y=140)

                                self.button7 = tk.Button(self.frame_tf, text="7", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button7)
                                self.button7.place(x=47, y=185)

                                self.button8 = tk.Button(self.frame_tf, text="8", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button8)
                                self.button8.place(x=97, y=185)

                                self.button9 = tk.Button(self.frame_tf, text="9", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button9)
                                self.button9.place(x=147, y=185)

                                self.button0 = tk.Button(self.frame_tf, text="0", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button00)
                                self.button0.place(x=97, y=230)

                                self.button_hapus = tk.Button(self.frame_tf, text="⬅", font=('Helvetica', 16, 'bold'), border=0,
                                                              activebackground="#e4b672",
                                                     activeforeground="white",bg="#e4b672", fg="white",
                                                              command=hapus111)
                                self.button_hapus.place(x=29, y=240)

                                self.button_submit = tk.Button(self.frame_tf, text="✅",font=('Helvetica', 16, 'bold'), border=0,
                                                              bg="#FDCB7F", fg="white",activebackground="#FDCB7F",
                                                     activeforeground="white",
                                                               command=submit_pin_tf)

                                self.button_submit.place(x=140, y=240)
                            
                            self.name = tk.Label(self.frame_konfirmasi, text=f'{self.login_username}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                     bg="white")
                            self.name.place(x=140, y=90)

                            self.no_rek = tk.Label(self.frame_konfirmasi, text=f'{myReke}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                      bg="white")
                            self.no_rek.place(x=140, y=120)
                                                
                            self.tujuan = tk.Label(self.frame_konfirmasi, text=f'TF To {norek}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                      bg="white")
                            self.tujuan.place(x=140, y=150)

                            self.nominal = tk.Label(self.frame_konfirmasi, text=f'{angka_terformat}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                      bg="white")
                            self.nominal.place(x=140, y=183)

                            self.back = tk.Button(self.frame_konfirmasi, text='Batal',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                      bg="#fdcb7f", fg='black',activebackground="#fdcb7f",
                                                                 activeforeground="black",command=batal_transaksi)
                            self.back.place(x=80, y=240)

                            self.next = tk.Button(self.frame_konfirmasi, text='Lanjut',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                      bg="#ffa41c", fg='black',activebackground="#ffa41c",
                                                                 activeforeground="black",command=next_transaksi)
                            self.next.place(x=310, y=240)                


                        else:
                                self.frame_9 = tk.Frame(self.mains)
                                self.frame_9.place(x=520, y=270)

                                bg3_image = Image.open("images\Frame 48.png")
                                resize_image = bg3_image.resize((219, 227))
                                self.photo2 = ImageTk.PhotoImage(resize_image)

                                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                self.lbl_frame.image = self.photo2
                                self.lbl_frame.pack()

                                def oouutt():
                                    self.frame_9.destroy()

                                self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                                self.outbut9.place(x=175, y=7)
                    else:
                            self.frame_9 = tk.Frame(self.mains)
                            self.frame_9.place(x=520, y=270)

                            bg3_image = Image.open("images\Frame 37.png")
                            resize_image = bg3_image.resize((219, 227))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            def oouutt():
                                self.frame_9.destroy()

                            self.outbut9 = tk.Button(self.frame_9,
                                                     font=('Helvetica'),
                                                     text="x",
                                                     fg="#ffffff",
                                                     bg="#FDCB7F",
                                                     border=0,
                                                     activebackground="#FDCB7F",
                                                     activeforeground="#ffffff",
                                                     cursor="hand2",
                                                     width=3,
                                                     command=oouutt)
                            self.outbut9.place(x=175, y=7)
                else:
                        self.frame_9 = tk.Frame(self.mains)
                        self.frame_9.place(x=520, y=270)

                        bg3_image = Image.open("images\Frame 49.png")
                        resize_image = bg3_image.resize((219, 227))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()

                        def oouutt():
                            self.frame_9.destroy()

                        self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                        self.outbut9.place(x=175, y=7)
            else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 36 (1).png")  #Firdaini Azmi (23031554071)
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                            self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                    self.outbut9.place(x=175, y=7)
        elif myReke==norek:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 76 (1).png")
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                self.outbut9.place(x=175, y=7)

        else:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 22.png")
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                self.outbut9.place(x=175, y=7)

    def depo(self):
        def pin_depo():
            def submit_pin_depo():
                PIN_tf2 = self.pin1_entry.get()
                nominalD = self.nominal_entry_depo.get()
                self.frame_pin_d.destroy()

                username = self.username_entry.get()
                password = self.hashingFunction(self.password_entry.get())
                locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                angka_terformat = locale.format_string('%d', int(nominalD), grouping=True)

                row = self.data_user.find_one({'username':username, 'password':password})
                myReke = row.get('nomor_rekening')
                myReke = int(myReke)
                
                random_number = random.randint(10000000,99999999)
                no_resiDepo=f'D-{random_number}'
                curent_time = time.strftime('%H:%M:%S')
                curent_date = time.strftime('%d-%m-%y')

                row_pin = self.data_user.find_one({'pin':PIN_tf2, 'username':username,'password':password})

                if row_pin is not None and PIN_tf2 is not None:
                    self.balance += int(nominalD)

                    self.data_user.update_one(
                        {"username": self.login_username},
                        {"$set": {"balance": self.balance}}
                    )

                    if self.click_count % 2 == 1:
                        self.show_balance()
                    else:
                        pass

                    self.create_history("Deposit", int(nominalD))
                    self.print_receipt(f'deposit',
                                        angka_terformat,no_resiDepo)
                    
                    self.frame_transaksi_p = tk.Frame(self.mains)
                    self.frame_transaksi_p.place(x=550, y=250)

                    bg3_image = Image.open("images\Frame 10.png")
                    resize_image = bg3_image.resize((211, 293))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbp_frame = tk.Label(self.frame_transaksi_p, image=self.photo2)
                    self.lbp_frame.image = self.photo2
                    self.lbp_frame.pack()

                    def left_transaksi_d():
                        self.frame_transaksi_p.destroy()
                    
                    self.leftP = tk.Button(self.frame_transaksi_p, text="X", font=('Helvetica', 10, 'bold'), bg="#e4b672",
                                                      fg="white",activebackground="#e4b672",
                                                             activeforeground="white",
                                            border=0, command=left_transaksi_d)
                    self.leftP.place(x=180, y=9)

                    self.nameP = tk.Label(self.frame_transaksi_p, text=f'{self.login_username}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                         bg="#fdcb7f")
                    self.nameP.place(x=80, y=75)

                    self.no_rekP = tk.Label(self.frame_transaksi_p, text=f'{myReke}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.no_rekP.place(x=80, y=97)
                    
                    self.tujuanP = tk.Label(self.frame_transaksi_p, text=f'Deposit',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.tujuanP.place(x=80, y=119)

                    self.nominalP = tk.Label(self.frame_transaksi_p, text=f'{angka_terformat}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.nominalP.place(x=80, y=139)

                    self.tanggalP = tk.Label(self.frame_transaksi_p, text=f'{curent_time}, {curent_date}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.tanggalP.place(x=80, y=160)

                    self.no_resiP = tk.Label(self.frame_transaksi_p, text=no_resiDepo, width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.no_resiP.place(x=80, y=183)

                    self.frame_d.destroy()
                        
                elif len(str(PIN_tf2)) != 6:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 29.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 34.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
            norek = self.norek_tujuan.get()
            username = self.username_entry.get()
            password = self.hashingFunction(self.password_entry.get())
            nominalD = self.nominal_entry_depo.get()

            row = self.data_user.find_one({"username":username,'password':password})

            myReke = row.get("nomor_rekening")
            myReke = int(myReke)
                
            if str(nominalD).isdigit():
                if int(nominalD) >= 10000:
                    locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                    angka_terformat = locale.format_string('%d', int(nominalD), grouping=True)

                    self.frame_konfirmasi_depo= tk.Frame(self.mains)
                    self.frame_konfirmasi_depo.place(x=420, y=200)

                    bg3_image = Image.open("images\Frame 47 (2).png")
                    resize_image = bg3_image.resize((520, 302))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbkd_frame = tk.Label(self.frame_konfirmasi_depo, image=self.photo2)
                    self.lbkd_frame.image = self.photo2
                    self.lbkd_frame.pack()

                    def left_transaksi_depo():
                        self.frame_konfirmasi_depo.destroy()
                    def batal_transaksi_depo():
                        self.frame_konfirmasi_depo.destroy()
                    def next_transaksi_depo():
                        self.frame_konfirmasi_depo.destroy()
                        self.frame_pin_d = tk.Frame(self.mains)
                        self.frame_pin_d.place(x=590, y=270)
                        def button11():
                            self.pin1_entry.insert(tk.END, 1)

                        def button12():
                            self.pin1_entry.insert(tk.END, 2)

                        def button13():
                            self.pin1_entry.insert(tk.END, 3)

                        def button14():
                            self.pin1_entry.insert(tk.END, 4)

                        def button15():
                            self.pin1_entry.insert(tk.END, 5)

                        def button16():
                            self.pin1_entry.insert(tk.END, 6)

                        def button17():
                            self.pin1_entry.insert(tk.END, 7)

                        def button18():
                            self.pin1_entry.insert(tk.END, 8)

                        def button19():
                            self.pin1_entry.insert(tk.END, 9)

                        def button20():
                            self.pin1_entry.insert(tk.END, 0)

                        def hapus1():
                            self.pin1_entry.delete(0, tk.END)

                        def leftpinDEPO():
                            self.frame_pin_d.destroy()
                        bg3_image = Image.open("images\Frame 9.png")
                        resize_image = bg3_image.resize((211, 293))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbd_frame = tk.Label(self.frame_pin_d, image=self.photo2)
                        self.lbd_frame.image = self.photo2
                        self.lbd_frame.pack()

                        self.left1_button= tk.Button(self.frame_pin_d, text="X", font=('Helvetica', 10, 'bold'), bg="#e4b672", fg="white",
                                                     activebackground="#e4b672",
                                                         activeforeground="white",border=0,
                                                 command=leftpinDEPO)
                        self.left1_button.place(x=186, y=13)

                        self.pin1_entry= tk.Entry(self.frame_pin_d, font=('Helvetica', 16, 'bold'), width=6, border=0, bg="#d9d9d9")
                        self.pin1_entry.place(x=68, y=52)

                        self.button11 = tk.Button(self.frame_pin_d, text="1", font=('Helvetica', 13, 'bold'), bg="#d9d9d9", border=0,
                                                 command=button11)
                        self.button11.place(x=47, y=97)

                        self.button12 = tk.Button(self.frame_pin_d, text="2", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                 command=button12)
                        self.button12.place(x=97, y=97)

                        self.button13 = tk.Button(self.frame_pin_d, text="3", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                 command=button13)
                        self.button13.place(x=147, y=95)

                        self.button14 = tk.Button(self.frame_pin_d, text="4", font=('Helvetica', 13, 'bold'), border=0,
                                                 command=button14)
                        self.button14.place(x=47, y=140)

                        self.button15 = tk.Button(self.frame_pin_d, text="5", font=('Helvetica', 13, 'bold'), border=0,
                                                 command=button15)
                        self.button15.place(x=97, y=140)

                        self.button16 = tk.Button(self.frame_pin_d, text="6", font=('Helvetica', 13, 'bold'), border=0,
                                                 command=button16)
                        self.button16.place(x=147, y=140)

                        self.button17 = tk.Button(self.frame_pin_d, text="7", font=('Helvetica', 13, 'bold'), border=0,
                                                 command=button17)
                        self.button17.place(x=47, y=185)

                        self.button18 = tk.Button(self.frame_pin_d, text="8", font=('Helvetica', 13, 'bold'), border=0,
                                                 command=button18)
                        self.button18.place(x=97, y=185)

                        self.button19 = tk.Button(self.frame_pin_d, text="9", font=('Helvetica', 13, 'bold'), border=0,
                                                 command=button19)
                        self.button19.place(x=147, y=185)

                        self.button20 = tk.Button(self.frame_pin_d, text="0", font=('Helvetica', 13, 'bold'), border=0,
                                                 command=button20)
                        self.button20.place(x=97, y=230)

                        self.button_hapus1 = tk.Button(self.frame_pin_d, text="⬅", font=('Helvetica', 16, 'bold'), border=0,
                                                      bg="#e4b672", fg="white",activebackground="#e4b672",
                                                         activeforeground="white",
                                                      command=hapus1)
                        self.button_hapus1.place(x=29, y=240)

                        self.button_submit1 = tk.Button(self.frame_pin_d, text="✅",font=('Helvetica', 16, 'bold'), border=0,
                                                        bg="#FDCB7F", fg="white",activebackground="#fdcb7f",
                                                         activeforeground="white",command=submit_pin_depo)
                        self.button_submit1.place(x=140, y=240)

                    self.name = tk.Label(self.frame_konfirmasi_depo, text=f'{self.login_username}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                             bg="white")
                    self.name.place(x=140, y=90)

                    self.no_rek = tk.Label(self.frame_konfirmasi_depo, text=f'{myReke}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                              bg="white")
                    self.no_rek.place(x=140, y=120)
                                        
                    self.tujuan = tk.Label(self.frame_konfirmasi_depo, text=f'Deposit',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                              bg="white")
                    self.tujuan.place(x=140, y=150)

                    self.nominal = tk.Label(self.frame_konfirmasi_depo, text=f'{angka_terformat}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                              bg="white")
                    self.nominal.place(x=140, y=183)

                    self.back = tk.Button(self.frame_konfirmasi_depo, text='Batal',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                              bg="#fdcb7f", fg='black',activebackground="#fdcb7f",
                                                         activeforeground="black",command=batal_transaksi_depo)
                    self.back.place(x=80, y=240)

                    self.next = tk.Button(self.frame_konfirmasi_depo, text='Lanjut',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                              bg="#ffa41c", fg='black',activebackground="#ffa41c",
                                                         activeforeground="black",command=next_transaksi_depo)
                    self.next.place(x=310, y=240)                

                else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 48.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)                        

                        
                    
                
            else:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 36 (1).png")  #Akmal Rizal (23031554078)
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                         font=('Helvetica'),
                                         text="x",
                                         fg="#ffffff",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="#ffffff",
                                         cursor="hand2",
                                         width=3,
                                         command=oouutt)
                self.outbut9.place(x=175, y=7)
        self.frame_d = tk.Frame(self.mains)
        self.frame_d.place(x=420, y=200)
        bg3_image = Image.open("images\Frame 14 (2).png")   #Akmal Rizal (23031554078)
        resize_image = bg3_image.resize((450, 300))
        self.photo2 = ImageTk.PhotoImage(resize_image)

        self.lbl_frame = tk.Label(self.frame_d, image=self.photo2)
        self.lbl_frame.image = self.photo2
        self.lbl_frame.pack()

        def left_frame_depo():
            self.frame_d.destroy()

        self.left1= tk.Button(self.frame_d, text="X", font=('Helvetica', 13, 'bold'),border=0, bg="#e8bf83", fg="white",activebackground="#e8bf83",
                                                     activeforeground="white",
                              command=left_frame_depo)
        self.left1.place(x=409, y=21)

        self.buttonD= tk.Button(self.frame_d, text="DEPOSIT",activebackground="#fdcb7f", activeforeground="white", width=18, font=('Helvetica', 17, 'bold'),
                                border=0, bg="#fdcb7f", fg="white", command=pin_depo)
        self.buttonD.place(x=95, y=163)
        
        self.nominal_entry_depo = tk.Entry(self.frame_d, width=17, border=0, bg="#ffffff", font=('Helvetica', 20))
        self.nominal_entry_depo.place(x=94, y=108)

    def withdraww(self):
        def pin_wd():
            def submit_pin_wd():
                PIN_w = self.pin2_entry.get()
                nominalW = self.nominal_entry_withdraw.get()
                self.frame_pin_w.destroy()

                username = self.username_entry.get()
                password = self.hashingFunction(self.password_entry.get())
                locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                angka_terformat = locale.format_string('%d', int(nominalW), grouping=True)

                row = self.data_user.find_one({'username':username,'password':password})
                myReke = row.get('nomor_rekening')
                myReke = int(myReke)
                
                random_number=random.randint(10000000,99999999)
                no_resiWD=f'W-{random_number}'
                curent_time=time.strftime('%H:%M:%S')
                curent_date=time.strftime('%d-%m-%y')

                row_pin = self.data_user.find_one({'pin':PIN_w, 'username':username,'password':password})

                if row_pin is not None and PIN_w is not None:
                    self.balance -= int(nominalW)

                    self.data_user.update_one(
                        {"username": self.login_username},
                        {"$set": {"balance": self.balance}}
                    )

                    if self.click_count % 2 == 1:
                        self.show_balance()
                    else:
                        pass

                    self.create_history("Withdrawal", int(nominalW))
                    self.print_receipt(f'withdraw',
                                       angka_terformat,
                                       no_resiWD)
                    
                    self.frame_transaksi_w = tk.Frame(self.mains)
                    self.frame_transaksi_w.place(x=550, y=250)

                    bg3_image = Image.open("images\Frame 10.png")
                    resize_image = bg3_image.resize((211, 293))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbw_frame = tk.Label(self.frame_transaksi_w, image=self.photo2)
                    self.lbw_frame.image = self.photo2
                    self.lbw_frame.pack()

                    def left_transaksi_w():
                        self.frame_transaksi_w.destroy()
                    
                    self.leftW = tk.Button(self.frame_transaksi_w, text="X", font=('Helvetica', 10, 'bold'), activebackground="#e4b672",
                                                             activeforeground="white",bg="#e4b672",
                                                      fg="white",
                                            border=0, command=left_transaksi_w)
                    self.leftW.place(x=180, y=9)

                    self.nameW = tk.Label(self.frame_transaksi_w,text=f'{self.login_username}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                         bg="#fdcb7f")
                    self.nameW.place(x=80, y=75)

                    self.no_rekW = tk.Label(self.frame_transaksi_w, text=f'{myReke}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.no_rekW.place(x=80, y=97)
                    
                    self.tujuanW = tk.Label(self.frame_transaksi_w, text=f'tarik tunai',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.tujuanW.place(x=80, y=119)

                    self.nominalW = tk.Label(self.frame_transaksi_w, text=f'{angka_terformat}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.nominalW.place(x=80, y=139)

                    self.tanggalW = tk.Label(self.frame_transaksi_w, text=f'{curent_time}, {curent_date}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.tanggalW.place(x=80, y=160)

                    self.no_resiW = tk.Label(self.frame_transaksi_w, text=no_resiWD,width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.no_resiW.place(x=80, y=183)

                    self.frame_w.destroy()
                        
                elif len(str(PIN_w)) != 6:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 29.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 34.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
            
            nominalW = self.nominal_entry_withdraw.get()
            norek = self.norek_tujuan.get()
            username = self.username_entry.get()
            password = self.hashingFunction(self.password_entry.get())

            row = self.data_user.find_one({'username':username,'password':password})
            myReke = row.get('nomor_rekening')
            myReke = int(myReke)

            if str(nominalW).isdigit():
                if self.balance >= int(nominalW):
                    if int(self.balance)-int(nominalW) >= 20000:
                        if int(nominalW) >= 10000:
                            locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                            angka_terformat = locale.format_string('%d', int(nominalW), grouping=True)

                            self.frame_konfirmasi_wd= tk.Frame(self.mains)
                            self.frame_konfirmasi_wd.place(x=420, y=200)

                            bg3_image = Image.open("images\Frame 47 (2).png")
                            resize_image = bg3_image.resize((520, 302))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbw_frame = tk.Label(self.frame_konfirmasi_wd, image=self.photo2)
                            self.lbw_frame.image = self.photo2
                            self.lbw_frame.pack()

                            def left_transaksi_wd():
                                self.frame_konfirmasi_wd.destroy()
                            def batal_transaksi_wd():
                                self.frame_konfirmasi_wd.destroy()
                            def next_transaksi_wd():
                                self.frame_konfirmasi_wd.destroy()
                                self.frame_pin_w = tk.Frame(self.mains)
                                self.frame_pin_w.place(x=590, y=270)
                                def button21():
                                    self.pin2_entry.insert(tk.END, 1)

                                def button22():
                                    self.pin2_entry.insert(tk.END, 2)

                                def button23():
                                    self.pin2_entry.insert(tk.END, 3)

                                def button24():
                                    self.pin2_entry.insert(tk.END, 4)

                                def button25():
                                    self.pin2_entry.insert(tk.END, 5)

                                def button26():
                                    self.pin2_entry.insert(tk.END, 6)

                                def button27():
                                    self.pin2_entry.insert(tk.END, 7)

                                def button28():
                                    self.pin2_entry.insert(tk.END, 8)

                                def button29():
                                    self.pin2_entry.insert(tk.END, 9)

                                def button30():
                                    self.pin2_entry.insert(tk.END, 0)

                                def hapusW():
                                    self.pin2_entry.delete(0, tk.END)

                                def left_pin_wd():
                                    self.frame_pin_w.destroy()

                                bg3_image = Image.open("images\Frame 9.png")
                                resize_image = bg3_image.resize((211, 293))
                                self.photo2 = ImageTk.PhotoImage(resize_image)

                                self.lbl_frame = tk.Label(self.frame_pin_w, image=self.photo2)
                                self.lbl_frame.image = self.photo2
                                self.lbl_frame.pack()
                                self.left3_button= tk.Button(self.frame_pin_w, text="X", font=('Helvetica', 10, 'bold'), bg="#e4b672", fg="white",
                                                            activebackground="#e4b672",
                                                         activeforeground="white",border=0,
                                                             command=left_pin_wd)
                                self.left3_button.place(x=186, y=13)

                                self.pin2_entry= tk.Entry(self.frame_pin_w, font=('Helvetica', 16, 'bold'), width=6, border=0, bg="#d9d9d9")
                                self.pin2_entry.place(x=68, y=52)

                                self.button21 = tk.Button(self.frame_pin_w, text="1", font=('Helvetica', 13, 'bold'), bg="#d9d9d9", border=0,
                                                         command=button21)
                                self.button21.place(x=47, y=97)

                                self.button22 = tk.Button(self.frame_pin_w, text="2", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                         command=button22)
                                self.button22.place(x=97, y=97)

                                self.button23 = tk.Button(self.frame_pin_w, text="3", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                         command=button23)
                                self.button23.place(x=147, y=95)

                                self.button24 = tk.Button(self.frame_pin_w, text="4", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button24)
                                self.button24.place(x=47, y=140)

                                self.button25 = tk.Button(self.frame_pin_w, text="5", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button25)
                                self.button25.place(x=97, y=140)

                                self.button26 = tk.Button(self.frame_pin_w, text="6", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button26)
                                self.button26.place(x=147, y=140)

                                self.button27 = tk.Button(self.frame_pin_w, text="7", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button27)
                                self.button27.place(x=47, y=185)

                                self.button28 = tk.Button(self.frame_pin_w, text="8", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button28)
                                self.button28.place(x=97, y=185)

                                self.button29 = tk.Button(self.frame_pin_w, text="9", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button29)
                                self.button29.place(x=147, y=185)

                                self.button30 = tk.Button(self.frame_pin_w, text="0", font=('Helvetica', 13, 'bold'), border=0,
                                                         command=button30)
                                self.button30.place(x=97, y=230)

                                self.button_hapus5 = tk.Button(self.frame_pin_w, text="⬅", font=('Helvetica', 16, 'bold'), border=0,
                                                                          bg="#e4b672", fg="white",activebackground="#e4b672",
                                                         activeforeground="white",
                                                              command=hapusW)
                                self.button_hapus5.place(x=29, y=240)

                                self.button_submit5 = tk.Button(self.frame_pin_w, text="✅",font=('Helvetica', 16, 'bold'), border=0,
                                                                bg="#FDCB7F", fg="white",activebackground="#fdcb7f",
                                                         activeforeground="white",command=submit_pin_wd)
                                self.button_submit5.place(x=140, y=240)
                            
                            self.name = tk.Label(self.frame_konfirmasi_wd, text=f'{self.login_username}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                             bg="white")
                            self.name.place(x=140, y=90)

                            self.no_rek = tk.Label(self.frame_konfirmasi_wd, text=f'{myReke}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                      bg="white")
                            self.no_rek.place(x=140, y=120)
                                                
                            self.tujuan = tk.Label(self.frame_konfirmasi_wd, text=f'Withdraw',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                      bg="white")
                            self.tujuan.place(x=140, y=150)

                            self.nominal = tk.Label(self.frame_konfirmasi_wd, text=f'{angka_terformat}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                      bg="white")
                            self.nominal.place(x=140, y=183)

                            self.back = tk.Button(self.frame_konfirmasi_wd, text='Batal',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                          bg="#fdcb7f", fg='black',activebackground="#fdcb7f",
                                                                     activeforeground="black",command=batal_transaksi_wd)
                            self.back.place(x=80, y=240)

                            self.next = tk.Button(self.frame_konfirmasi_wd, text='Lanjut',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                          bg="#ffa41c", fg='black',activebackground="#ffa41c",
                                                                     activeforeground="black",command=next_transaksi_wd)
                            self.next.place(x=310, y=240)

                        else:
                            self.frame_9 = tk.Frame(self.mains)
                            self.frame_9.place(x=520, y=270)

                            bg3_image = Image.open("images\Frame 48.png")
                            resize_image = bg3_image.resize((219, 227))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            def oouutt():
                                self.frame_9.destroy()

                            self.outbut9 = tk.Button(self.frame_9,
                                                     font=('Helvetica'),
                                                     text="x",
                                                     fg="#ffffff",
                                                     bg="#FDCB7F",
                                                     border=0,
                                                     activebackground="#FDCB7F",
                                                     activeforeground="#ffffff",
                                                     cursor="hand2",
                                                     width=3,
                                                     command=oouutt)
                            self.outbut9.place(x=175, y=7)
                    else:
                        self.frame_9 = tk.Frame(self.mains)
                        self.frame_9.place(x=520, y=270)

                        bg3_image = Image.open("images\Frame 49.png")
                        resize_image = bg3_image.resize((219, 227))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()

                        def oouutt():
                            self.frame_9.destroy()

                        self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                        self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 37.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                    self.outbut9.place(x=175, y=7)
                   
            else:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 36 (1).png")   #Nova Aulia Agustin (23031554022)
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                        self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                                     font=('Helvetica'),
                                                     text="x",
                                                     fg="#ffffff",
                                                     bg="#FDCB7F",
                                                     border=0,
                                                     activebackground="#FDCB7F",
                                                     activeforeground="#ffffff",
                                                     cursor="hand2",
                                                     width=3,
                                                     command=oouutt)
                self.outbut9.place(x=175, y=7)
        self.frame_w = tk.Frame(self.mains)
        self.frame_w.place(x=420, y=200)
        bg3_image = Image.open("images\Frame 15 (5).png")  #Nova Aulia Agustin (23031554022)
        resize_image = bg3_image.resize((450, 300))
        self.photo2 = ImageTk.PhotoImage(resize_image)

        def left_frame_withdraw():
            self.frame_w.destroy()

        self.lbl_frame = tk.Label(self.frame_w, image=self.photo2)
        self.lbl_frame.image = self.photo2
        self.lbl_frame.pack()

        self.left2= tk.Button(self.frame_w, text="X", font=('Helvetica', 13, 'bold'),border=0, bg="#e8bf83", fg="white",
                              activebackground="#e8bf83",
                                                     activeforeground="white",
                              command=left_frame_withdraw)
        self.left2.place(x=409, y=21)

        self.buttonW= tk.Button(self.frame_w, text="WITHDRAW",activebackground="#fdcb7f", activeforeground="white", width=18, font=('Helvetica', 17, 'bold'),
                                border=0, bg="#fdcb7f", fg="white", command=pin_wd)
        self.buttonW.place(x=95, y=163)
        
        self.nominal_entry_withdraw = tk.Entry(self.frame_w, width=17, border=0, bg="#ffffff", font=('Helvetica', 20))
        self.nominal_entry_withdraw.place(x=94, y=108)

    def Ecommerce(self):
        self.frame_e = tk.Frame(self.mains)
        self.frame_e.place(x=400, y=90)

        bg3_image = Image.open("images\Frame 16 (1).png")
        resize_image = bg3_image.resize((528, 628))
        self.photo2 = ImageTk.PhotoImage(resize_image)

        self.lbl_frame = tk.Label(self.frame_e, image=self.photo2)
        self.lbl_frame.image = self.photo2
        self.lbl_frame.pack()

        def quit_eccomerce():
            self.frame_e.destroy()

        self.buy_pulsa_button = tk.Button(self.frame_e,
                                        text='Pulsa',
                                        font=("Helvetica", 17,'bold'),
                                        fg="#ffffff",
                                        bg="#FDCB7F",
                                        border=0,
                                        activebackground="#FDCB7F",
                                        activeforeground="#ffffff",
                                        cursor="hand2",
                                        width=22,
                                        command=self.beliPulsa)
        self.buy_pulsa_button.place(x=105, y=107)

        self.buy_listrik_button = tk.Button(self.frame_e,
                                            text='Beli Listrik',
                                            font=("Helvetica", 17, 'bold'),
                                            fg="#ffffff",
                                            bg="#FDCB7F",
                                            border=0,
                                            activebackground="#FDCB7F",
                                            activeforeground="#ffffff",
                                            cursor="hand2",
                                            width=22,
                                            command=self.beliListrik)
        self.buy_listrik_button.place(x=105, y=190)

        self.quit_ecommerce_button = tk.Button(self.frame_e,
                                     text='X',
                                     font=("Helvetica", 21,'bold'),
                                     fg="#ffffff",
                                     bg="#FDCB7F",
                                     border=0,
                                     activebackground="#FDCB7F",
                                     activeforeground="#ffffff",
                                     cursor="hand2",
                                     width=3,
                                     command=quit_eccomerce)
        self.quit_ecommerce_button.place(x=473, y=9)

    def beliPulsa(self):
        def pinP():
            def submitP():
                PIN_Pul = self.pinP_entry.get()
                nominalP= self.nominal_pulsa.get()
                self.frame_pin_p.destroy()

                username = self.username_entry.get()
                password = self.hashingFunction(self.password_entry.get())

                locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                angka_terformat=locale.format_string('%d', int(nominalP), grouping=True)

                row = self.data_user.find_one({'username':username, 'password':password})
                myReke = row.get('nomor_rekening')
                myReke = int(myReke)
                
                random_number=random.randint(10000000,99999999)
                no_resiP=f'P-{random_number}'
                curent_time=time.strftime('%H:%M:%S')
                curent_date=time.strftime('%d-%m-%y')
                self.frame_p.destroy()

                row_pin = self.data_user.find_one({'pin':PIN_Pul, 'username':username,'password':password})

                if row_pin is not None and PIN_Pul is not None:
                    self.balance -= int(nominalP)

                    self.data_user.update_one(
                        {"username": self.login_username},
                        {"$set": {"balance": self.balance}}
                    )

                    if self.click_count % 2 == 1:
                        self.show_balance()
                    else:
                        pass

                    self.create_history("Pulsa", int(nominalP))
                    self.print_receipt(f'pulsa',
                                      angka_terformat, no_resiP)

                    self.frame_transaksi_p = tk.Frame(self.mains)
                    self.frame_transaksi_p.place(x=550, y=250)

                    bg3_image = Image.open("images\Frame 10.png")
                    resize_image = bg3_image.resize((211, 293))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    def left_transaksiP():
                        self.frame_transaksi_p.destroy()

                    self.lbp_frame = tk.Label(self.frame_transaksi_p, image=self.photo2)
                    self.lbp_frame.image = self.photo2
                    self.lbp_frame.pack()
                    
                    self.leftP = tk.Button(self.frame_transaksi_p,
                                           text="X",
                                           font=('Helvetica', 10, 'bold'),
                                           bg="#e4b672",
                                           fg="white",
                                           activebackground="#e4b672",
                                           activeforeground="white",
                                           border=0, command=left_transaksiP)
                    self.leftP.place(x=180, y=9)

                    self.nameP = tk.Label(self.frame_transaksi_p,text=f'{self.login_username}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                         bg="#fdcb7f")
                    self.nameP.place(x=80, y=75)

                    self.no_rekP = tk.Label(self.frame_transaksi_p, text=f'{myReke}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.no_rekP.place(x=80, y=97)
                    
                    self.tujuanP = tk.Label(self.frame_transaksi_p, text=f'PEMBELIAN PULSA',width=20, border=0, anchor='w', font=('Helvetica', 8),
                                                          bg="#fdcb7f")
                    self.tujuanP.place(x=80, y=119)

                    self.nominalP = tk.Label(self.frame_transaksi_p, text=f'{angka_terformat}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.nominalP.place(x=80, y=139)

                    self.tanggalP = tk.Label(self.frame_transaksi_p, text=f'{curent_time}, {curent_date}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.tanggalP.place(x=80, y=160)

                    self.no_resiP = tk.Label(self.frame_transaksi_p, text=no_resiP,width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.no_resiP.place(x=80, y=183)

                    self.frame_e.destroy()

                elif len(str(PIN_Pul)) != 6:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 29.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 34.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
            
            nominalP = self.nominal_pulsa.get()
            noHP=self.no_HP.get()
            norek = self.norek_tujuan.get()
            username = self.username_entry.get()
            password = self.hashingFunction(self.password_entry.get())

            row = self.data_user.find_one({'username':username, 'password':password})
            myReke = row.get('nomor_rekening')
            myReke = int(myReke)

            if str(nominalP).isdigit():
                if self.balance >= int(nominalP):
                    if int(self.balance)-int(nominalP) >= 20000:
                        if int(nominalP) >= 10000:
                            if str(noHP).isdigit():
                                if 12<= len(str(noHP)) <=13:
                                    locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                                    angka_terformat = locale.format_string('%d', int(nominalP), grouping=True)

                                    self.frame_konfirmasi_pulsa= tk.Frame(self.mains)
                                    self.frame_konfirmasi_pulsa.place(x=420, y=200)

                                    bg3_image = Image.open("images\Frame 47 (2).png")
                                    resize_image = bg3_image.resize((520, 302))
                                    self.photo2 = ImageTk.PhotoImage(resize_image)

                                    self.lbp_frame = tk.Label(self.frame_konfirmasi_pulsa, image=self.photo2)
                                    self.lbp_frame.image = self.photo2
                                    self.lbp_frame.pack()

                                    def left_transaksi_p():
                                        self.frame_konfirmasi_pulsa.destroy()
                                    def batal_transaksi_p():
                                        self.frame_konfirmasi_pulsa.destroy()
                                    def next_transaksi_p():
                                        self.frame_konfirmasi_pulsa.destroy()
                                        self.frame_pin_p = tk.Frame(self.mains)
                                        self.frame_pin_p.place(x=590, y=270)
                                        def left_transaksiP():
                                            self.frame_transaksi_p.destroy()
                                            
                                        def buttonP1():
                                            self.pinP_entry.insert(tk.END, 1)

                                        def buttonP2():
                                            self.pinP_entry.insert(tk.END, 2)

                                        def buttonP3():
                                            self.pinP_entry.insert(tk.END, 3)

                                        def buttonP4():
                                            self.pinP_entry.insert(tk.END, 4)

                                        def buttonP5():
                                            self.pinP_entry.insert(tk.END, 5)

                                        def buttonP6():
                                            self.pinP_entry.insert(tk.END, 6)

                                        def buttonP7():
                                            self.pinP_entry.insert(tk.END, 7)

                                        def buttonP8():
                                            self.pinP_entry.insert(tk.END, 8)

                                        def buttonP9():
                                            self.pinP_entry.insert(tk.END, 9)

                                        def buttonP0():
                                            self.pinP_entry.insert(tk.END, 0)

                                        def hapusP():
                                            self.pinP_entry.delete(0, tk.END)

                                        def leftP():
                                            self.frame_pin_p.destroy()

                                        bg3_image = Image.open("images\Frame 9.png")
                                        resize_image = bg3_image.resize((211, 293))
                                        self.photo2 = ImageTk.PhotoImage(resize_image)

                                        self.lbP_frame = tk.Label(self.frame_pin_p, image=self.photo2)
                                        self.lbP_frame.image = self.photo2
                                        self.lbP_frame.pack()

                                        self.leftP_button= tk.Button(self.frame_pin_p, text="X", font=('Helvetica', 10, 'bold'), bg="#e4b672", fg="white",
                                                                     activebackground="#e4b672",
                                                             activeforeground="white",border=0,
                                                                     command=leftP)
                                        self.leftP_button.place(x=186, y=13)

                                        self.pinP_entry= tk.Entry(self.frame_pin_p, font=('Helvetica', 16, 'bold'), width=6, border=0, bg="#d9d9d9")
                                        self.pinP_entry.place(x=68, y=52)

                                        self.buttonP1 = tk.Button(self.frame_pin_p, text="1", font=('Helvetica', 13, 'bold'), bg="#d9d9d9", border=0,
                                                                 command=buttonP1)
                                        self.buttonP1.place(x=47, y=97)
                                        self.buttonP2 = tk.Button(self.frame_pin_p, text="2", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                                 command=buttonP2)
                                        self.buttonP2.place(x=97, y=97)

                                        self.buttonP3 = tk.Button(self.frame_pin_p, text="3", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                                 command=buttonP3)
                                        self.buttonP3.place(x=147, y=95)

                                        self.buttonP4 = tk.Button(self.frame_pin_p, text="4", font=('Helvetica', 13, 'bold'), border=0,
                                                                 command=buttonP4)
                                        self.buttonP4.place(x=47, y=140)

                                        self.buttonP5 = tk.Button(self.frame_pin_p, text="5", font=('Helvetica', 13, 'bold'), border=0,
                                                                 command=buttonP5)
                                        self.buttonP5.place(x=97, y=140)

                                        self.buttonP6 = tk.Button(self.frame_pin_p, text="6", font=('Helvetica', 13, 'bold'), border=0,
                                                                 command=buttonP6)
                                        self.buttonP6.place(x=147, y=140)

                                        self.buttonP7 = tk.Button(self.frame_pin_p, text="7", font=('Helvetica', 13, 'bold'), border=0,
                                                                 command=buttonP7)
                                        self.buttonP7.place(x=47, y=185)

                                        self.buttonP8= tk.Button(self.frame_pin_p, text="8", font=('Helvetica', 13, 'bold'), border=0,
                                                                 command=buttonP8)
                                        self.buttonP8.place(x=97, y=185)

                                        self.buttonP9 = tk.Button(self.frame_pin_p, text="9", font=('Helvetica', 13, 'bold'), border=0,
                                                                 command=buttonP9)
                                        self.buttonP9.place(x=147, y=185)

                                        self.buttonP0 = tk.Button(self.frame_pin_p, text="0", font=('Helvetica', 13, 'bold'), border=0,
                                                                 command=buttonP0)
                                        self.buttonP0.place(x=97, y=230)

                                        self.button_hapusP = tk.Button(self.frame_pin_p, text="⬅", font=('Helvetica', 15, 'bold'), border=0,
                                                                      bg="#e4b672",fg='black',activebackground="#e4b672",
                                                             activeforeground="black",
                                                                      command=hapusP)
                                        self.button_hapusP.place(x=29, y=240)

                                        self.button_submitP = tk.Button(self.frame_pin_p, text="✅", font=('Helvetica', 15, 'bold'), border=0,
                                                                       bg="#FDCB7F", fg='black',activebackground="#fdcb7f",
                                                             activeforeground="black",command=submitP)
                                        self.button_submitP.place(x=140, y=240)
                                    self.name = tk.Label(self.frame_konfirmasi_pulsa, text=f'{self.login_username}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                 bg="white")
                                    self.name.place(x=140, y=90)

                                    self.no_rek = tk.Label(self.frame_konfirmasi_pulsa, text=f'{myReke}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                              bg="white")
                                    self.no_rek.place(x=140, y=120)
                                                        
                                    self.tujuan = tk.Label(self.frame_konfirmasi_pulsa, text=f'Pembelian Pulsa',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                              bg="white")
                                    self.tujuan.place(x=140, y=150)

                                    self.nominal = tk.Label(self.frame_konfirmasi_pulsa, text=f'{angka_terformat}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                              bg="white")
                                    self.nominal.place(x=140, y=183)

                                    self.back = tk.Button(self.frame_konfirmasi_pulsa, text='Batal',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                              bg="#fdcb7f", fg='black',activebackground="#fdcb7f",
                                                                         activeforeground="black",command=batal_transaksi_p)
                                    self.back.place(x=80, y=240)

                                    self.next = tk.Button(self.frame_konfirmasi_pulsa, text='Lanjut',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                              bg="#ffa41c", fg='black',activebackground="#ffa41c",
                                                                         activeforeground="black",command=next_transaksi_p)
                                    self.next.place(x=310, y=240)
                                else:
                                    self.frame_9 = tk.Frame(self.mains)
                                    self.frame_9.place(x=520, y=270)

                                    bg3_image = Image.open("images\Frame 21.png")
                                    resize_image = bg3_image.resize((219, 227))
                                    self.photo2 = ImageTk.PhotoImage(resize_image)

                                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                    self.lbl_frame.image = self.photo2
                                    self.lbl_frame.pack()

                                    def oouutt():
                                        self.frame_9.destroy()

                                    self.outbut9 = tk.Button(self.frame_9,
                                                             font=('Helvetica'),
                                                             text="x",
                                                             fg="#ffffff",
                                                             bg="#FDCB7F",
                                                             border=0,
                                                             activebackground="#FDCB7F",
                                                             activeforeground="#ffffff",
                                                             cursor="hand2",
                                                             width=3,
                                                             command=oouutt)
                                    self.outbut9.place(x=175, y=7)
                            else:
                                self.frame_9 = tk.Frame(self.mains)
                                self.frame_9.place(x=520, y=270)

                                bg3_image = Image.open("images\Frame 41.png")
                                resize_image = bg3_image.resize((219, 227))
                                self.photo2 = ImageTk.PhotoImage(resize_image)

                                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                self.lbl_frame.image = self.photo2
                                self.lbl_frame.pack()

                                def oouutt():
                                    self.frame_9.destroy()

                                self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                                self.outbut9.place(x=175, y=7)
                        else:
                            self.frame_9 = tk.Frame(self.mains)
                            self.frame_9.place(x=520, y=270)

                            bg3_image = Image.open("images\Frame 48.png")
                            resize_image = bg3_image.resize((219, 227))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            def oouutt():
                                self.frame_9.destroy()

                            self.outbut9 = tk.Button(self.frame_9,
                                                     font=('Helvetica'),
                                                     text="x",
                                                     fg="#ffffff",
                                                     bg="#FDCB7F",
                                                     border=0,
                                                     activebackground="#FDCB7F",
                                                     activeforeground="#ffffff",
                                                     cursor="hand2",
                                                     width=3,
                                                     command=oouutt)
                            self.outbut9.place(x=175, y=7)
                    else:
                        self.frame_9 = tk.Frame(self.mains)
                        self.frame_9.place(x=520, y=270)

                        bg3_image = Image.open("images\Frame 49.png")
                        resize_image = bg3_image.resize((219, 227))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()

                        def oouutt():
                            self.frame_9.destroy()

                        self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                        self.outbut9.place(x=175, y=7)
                else:
                        self.frame_9 = tk.Frame(self.mains)
                        self.frame_9.place(x=520, y=270)

                        bg3_image = Image.open("images\Frame 37.png")
                        resize_image = bg3_image.resize((219, 227))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()

                        def oouutt():
                            self.frame_9.destroy()

                        self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                        self.outbut9.place(x=175, y=7)
            else:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 36 (1).png")  #Muhammad Fabyan Putroagung (23031554029)
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                         font=('Helvetica'),
                                         text="x",
                                         fg="#ffffff",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="#ffffff",
                                         cursor="hand2",
                                         width=3,
                                         command=oouutt)
                self.outbut9.place(x=175, y=7)

        self.frame_p = tk.Frame(self.mains)
        self.frame_p.place(x=400, y=90)
        bg3_image = Image.open("images\Frame 17 (2).png")       #Muhammad Fabyan Putroagung (23031554029)
        resize_image = bg3_image.resize((520, 620))
        self.photo2 = ImageTk.PhotoImage(resize_image)

        self.lbl_frame = tk.Label(self.frame_p, image=self.photo2)
        self.lbl_frame.image = self.photo2
        self.lbl_frame.pack()

        def nomPul(e):
            nim = self.nominal_pulsa.get()
            if nim == "Nominal":
                self.nominal_pulsa.delete(0,"end")
        #
        def nomPul_zoomout(e):
            name = self.nominal_pulsa.get()
            if name == "":
                self.nominal_pulsa.insert(0,"Nominal")

        def noHP(e):
            hp = self.no_HP.get()
            if hp == "No. Handphone":
                self.no_HP.delete(0,"end")
        #
        def noHP_zoomout(e):
            name = self.no_HP.get()
            if name == "":
                self.no_HP.insert(0,"No. Handphone")

        def quit_pulsa():
            self.frame_p.destroy()

        self.nominal_pulsa = tk.Entry(self.frame_p,
                                font=('Helvetica', 20),
                                fg="#777777",
                                bg="white",
                                width=19,
                                border=0,)
        self.nominal_pulsa.place(y=194, x=118)
        self.nominal_pulsa.insert(0, "Nominal")
        self.nominal_pulsa.bind('<FocusIn>', nomPul)
        self.nominal_pulsa.bind('<FocusOut>', nomPul_zoomout)

        self.no_HP = tk.Entry(self.frame_p,
                                     font=('Helvetica', 20),
                                     fg="#777777",
                                     bg="white",
                                     width=19,
                                     border=0
                                     )
        self.no_HP.place(x=118,y=279)
        self.no_HP.insert(0, "No. Handphone")
        self.no_HP.bind('<FocusIn>', noHP)
        self.no_HP.bind('<FocusOut>', noHP_zoomout)

        self.nextButt_buyPulsa = tk.Button(self.frame_p,
                                          text='Lanjut',
                                          font=("Helvetica", 17, 'bold'),
                                          fg="#ffffff",
                                          bg="#FDCB7F",
                                          border=0,
                                          activebackground="#FDCB7F",
                                          activeforeground="#ffffff",
                                          cursor="hand2",
                                          width=21,
                                          command=pinP)
        self.nextButt_buyPulsa.place(x=110, y=357)

        self.quit_pulsa_button = tk.Button(self.frame_p,
                                               text='X',
                                               font=("Helvetica", 21, 'bold'),
                                               fg="#ffffff",
                                               bg="#FDCB7F",
                                               border=0,
                                               activebackground="#FDCB7F",
                                               activeforeground="#ffffff",
                                               cursor="hand2",
                                               width=3,
                                            command=quit_pulsa)
        self.quit_pulsa_button.place(x=465, y=9)

    def beliListrik(self):
        def pinL():
            def submitL():
                PIN_Lis = self.pinL_entry.get()
                nominalL= self.nominal_listrik.get()
                self.frame_pin_l.destroy()

                username = self.username_entry.get()
                password = self.hashingFunction(self.password_entry.get())
                locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                angka_terformat = locale.format_string('%d', int(nominalL), grouping=True)

                row = self.data_user.find_one({'username':username, 'password':password})
                myReke = row.get('nomor_rekening')
                myReke = int(myReke)
                
                random_number=random.randint(10000000,99999999)
                no_resiL=f'L-{random_number}'
                curent_time=time.strftime('%H:%M:%S')
                curent_date=time.strftime('%d-%m-%y')
                self.frame_l.destroy()

                row_pin = self.data_user.find_one({'pin':PIN_Lis, 'username':username,'password':password})

                if row_pin is not None and PIN_Lis is not None:
                    self.balance-=int(nominalL)

                    self.data_user.update_one(
                        {"username": self.login_username},
                        {"$set": {"balance": self.balance}}
                    )

                    if self.click_count % 2 == 1:
                        self.show_balance()
                    else:
                        pass

                    token_number = random.randint(00000000000000000000, 99999999999999999999)
                    formatted_number = f'{token_number:020}'
                    results = '-'.join([formatted_number[i:i + 4] for i in range(0, len(formatted_number), 4)])

                    self.print_receipt_for_buy_listrik('Pembelian Pulsa Listrik',
                                       angka_terformat,
                                       results,
                                       no_resiL)
                    self.create_history("Listrik", int(nominalL))

                    self.frame_transaksi_l = tk.Frame(self.mains)
                    self.frame_transaksi_l.place(x=550, y=250)

                    bg3_image = Image.open("images\Frame 10.png")
                    resize_image = bg3_image.resize((211, 293))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_transaksi_l, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def left_transaksi_l():
                        self.frame_transaksi_l.destroy()
                    
                    self.leftL = tk.Button(self.frame_transaksi_l, text="X", font=('Helvetica', 10, 'bold'), bg="#e4b672",
                                                      fg="white",activebackground="#e4b672",
                                                             activeforeground="white",
                                            border=0, command=left_transaksi_l)
                    self.leftL.place(x=180, y=9)

                    self.nameL = tk.Label(self.frame_transaksi_l,text=f'{self.login_username}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                         bg="#fdcb7f")
                    self.nameL.place(x=80, y=75)

                    self.no_rekL = tk.Label(self.frame_transaksi_l, text=f'{myReke}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                      bg="#fdcb7f")
                    self.no_rekL.place(x=80, y=97)
                    
                    self.tujuanL = tk.Label(self.frame_transaksi_l, text=f'Pembelian Token Listrik',width=21, border=0, anchor='w', font=('Helvetica', 8),
                                                          bg="#fdcb7f")
                    self.tujuanL.place(x=80, y=119)

                    self.nominalL = tk.Label(self.frame_transaksi_l, text=f'{angka_terformat}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.nominalL.place(x=80, y=139)

                    self.tanggalL= tk.Label(self.frame_transaksi_l, text=f'{curent_time}, {curent_date}',width=18, border=0, anchor='w', font=('Helvetica', 9),
                                                          bg="#fdcb7f")
                    self.tanggalL.place(x=80, y=160)

                    self.no_resiL = tk.Label(self.frame_transaksi_l, text=no_resiL,width=18, border=0, anchor='w', font=('Helvetica',9),
                                                          bg="#fdcb7f")
                    self.no_resiL.place(x=80, y=183)

                    self.name_tokenL = tk.Label(self.frame_transaksi_l, text='No. Token',width=15, border=0, anchor='w', font=('Helvetica', 10),
                                                          bg="#fdcb7f")
                    self.name_tokenL.place(x=80, y=220)

                    self.no_tokenL = tk.Label(self.frame_transaksi_l, text=f'{results}',width=22, border=0, anchor='w', font=('Helvetica', 10),
                                                          bg="#fdcb7f")
                    self.no_tokenL.place(x=30, y=240)

                    self.frame_l.destroy()
                    self.frame_e.destroy()
                        
                elif len(str(PIN_Lis)) != 6:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 29.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 34.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
            nominalL = self.nominal_listrik.get()
            tokenL=self.no_token_listrik.get()
            norek = self.norek_tujuan.get()
            username = self.username_entry.get()
            password = self.hashingFunction(self.password_entry.get())

            row = self.data_user.find_one({'username': username, 'password': password})
            myReke = row.get('nomor_rekening')
            myReke = int(myReke)
            
            if str(nominalL).isdigit():
                if self.balance >= int(nominalL):
                    if int(self.balance)-int(nominalL) >= 20000:
                        if int(nominalL) >= 10000:
                            if str(tokenL).isdigit():
                                if 12<= len(tokenL) <=13:
                                        locale.setlocale(locale.LC_NUMERIC, 'id_ID')
                                        angka_terformat = locale.format_string('%d', int(nominalL), grouping=True)

                                        self.frame_konfirmasi_listrik= tk.Frame(self.mains)
                                        self.frame_konfirmasi_listrik.place(x=420, y=200)

                                        bg3_image = Image.open("images\Frame 47 (2).png")
                                        resize_image = bg3_image.resize((520, 302))
                                        self.photo2 = ImageTk.PhotoImage(resize_image)   

                                        self.lbl_frame = tk.Label(self.frame_konfirmasi_listrik, image=self.photo2)
                                        self.lbl_frame.image = self.photo2
                                        self.lbl_frame.pack()

                                        def batal_transaksi_l():
                                            self.frame_konfirmasi_listrik.destroy()
                                        def next_transaksi_l():
                                            self.frame_konfirmasi_listrik.destroy()
                                            self.frame_pin_l = tk.Frame(self.mains)
                                            self.frame_pin_l.place(x=590, y=270)

                                            def left_transaksi_l():
                                                self.frame_transaksi_l.destroy()

                                            def buttonL1():
                                                self.pinL_entry.insert(tk.END, 1)

                                            def buttonL2():
                                                self.pinL_entry.insert(tk.END, 2)

                                            def buttonL3():
                                                self.pinL_entry.insert(tk.END, 3)

                                            def buttonL4():
                                                self.pinL_entry.insert(tk.END, 4)

                                            def buttonL5():
                                                self.pinL_entry.insert(tk.END, 5)

                                            def buttonL6():
                                                self.pinL_entry.insert(tk.END, 6)

                                            def buttonL7():
                                                self.pinL_entry.insert(tk.END, 7)

                                            def buttonL8():
                                                self.pinL_entry.insert(tk.END, 8)

                                            def buttonL9():
                                                self.pinL_entry.insert(tk.END, 9)

                                            def buttonL0():
                                                self.pinL_entry.insert(tk.END, 0)

                                            def hapusL():
                                                self.pinL_entry.delete(0, tk.END)

                                            def leftL():
                                                self.frame_pin_l.destroy()

                                            bg3_image = Image.open("images\Frame 9.png")
                                            resize_image = bg3_image.resize((211, 293))
                                            self.photo2 = ImageTk.PhotoImage(resize_image)

                                            self.lbl_frame = tk.Label(self.frame_pin_l, image=self.photo2)
                                            self.lbl_frame.image = self.photo2
                                            self.lbl_frame.pack()

                                            self.leftL_button= tk.Button(self.frame_pin_l, text="X", font=('Helvetica', 10, 'bold'), bg="#e4b672", fg="white",
                                                                     activebackground="#e4b672",
                                                             activeforeground="white",border=0,
                                                                         command=leftL)
                                            self.leftL_button.place(x=186, y=13)

                                            self.pinL_entry= tk.Entry(self.frame_pin_l, font=('Helvetica', 16, 'bold'), width=6, border=0, bg="#d9d9d9")
                                            self.pinL_entry.place(x=68, y=52)

                                            self.buttonL1 = tk.Button(self.frame_pin_l, text="1", font=('Helvetica', 13, 'bold'), bg="#d9d9d9", border=0,
                                                                 command=buttonL1)
                                            self.buttonL1.place(x=47, y=97)
                                            self.buttonL2 = tk.Button(self.frame_pin_l, text="2", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                                     command=buttonL2)
                                            self.buttonL2.place(x=97, y=97)

                                            self.buttonL3 = tk.Button(self.frame_pin_l, text="3", font=('Helvetica', 13, 'bold'), border=0, bg="#d9d9d9",
                                                                     command=buttonL3)
                                            self.buttonL3.place(x=147, y=95)

                                            self.buttonL4 = tk.Button(self.frame_pin_l, text="4", font=('Helvetica', 13, 'bold'), border=0,
                                                                     command=buttonL4)
                                            self.buttonL4.place(x=47, y=140)

                                            self.buttonL5 = tk.Button(self.frame_pin_l, text="5", font=('Helvetica', 13, 'bold'), border=0,
                                                                     command=buttonL5)
                                            self.buttonL5.place(x=97, y=140)

                                            self.buttonL6 = tk.Button(self.frame_pin_l, text="6", font=('Helvetica', 13, 'bold'), border=0,
                                                                     command=buttonL6)
                                            self.buttonL6.place(x=147, y=140)

                                            self.buttonL7 = tk.Button(self.frame_pin_l, text="7", font=('Helvetica', 13, 'bold'), border=0,
                                                                     command=buttonL7)
                                            self.buttonL7.place(x=47, y=185)

                                            self.buttonL8= tk.Button(self.frame_pin_l, text="8", font=('Helvetica', 13, 'bold'), border=0,
                                                                     command=buttonL8)
                                            self.buttonL8.place(x=97, y=185)

                                            self.buttonL9 = tk.Button(self.frame_pin_l, text="9", font=('Helvetica', 13, 'bold'), border=0,
                                                                     command=buttonL9)
                                            self.buttonL9.place(x=147, y=185)

                                            self.buttonL0 = tk.Button(self.frame_pin_l, text="0", font=('Helvetica', 13, 'bold'), border=0,
                                                                     command=buttonL0)
                                            self.buttonL0.place(x=97, y=230)

                                            self.button_hapusL = tk.Button(self.frame_pin_l, text="⬅", font=('Helvetica', 15, 'bold'), border=0,
                                                                          bg="#e4b672",fg='black',activebackground="#e4b672",
                                                             activeforeground="black",
                                                                          command=hapusL)
                                            self.button_hapusL.place(x=29, y=240)

                                            self.button_submitL = tk.Button(self.frame_pin_l, text="✅", font=('Helvetica', 15, 'bold'), border=0,
                                                                            bg="#FDCB7F",fg='black',activebackground="#fdcb7f",
                                                             activeforeground="black",
                                                                           command=submitL)
                                            self.button_submitL.place(x=140, y=240)
                                        self.name = tk.Label(self.frame_konfirmasi_listrik, text=f'{self.login_username}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                 bg="white")
                                        self.name.place(x=140, y=90)

                                        self.no_rek = tk.Label(self.frame_konfirmasi_listrik, text=f'{myReke}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                                  bg="white")
                                        self.no_rek.place(x=140, y=120)
                                                            
                                        self.tujuan = tk.Label(self.frame_konfirmasi_listrik, text=f'Pembelian Listrik',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                                  bg="white")
                                        self.tujuan.place(x=140, y=150)

                                        self.nominal = tk.Label(self.frame_konfirmasi_listrik, text=f'{angka_terformat}',width=24, border=0, anchor='w', font=('Helvetica', 18,'bold'),
                                                                                                  bg="white")
                                        self.nominal.place(x=140, y=183)

                                        self.back = tk.Button(self.frame_konfirmasi_listrik, text='Batal',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                              bg="#fdcb7f", fg='black',activebackground="#fdcb7f",
                                                                         activeforeground="black",command=batal_transaksi_l)
                                        self.back.place(x=80, y=240)

                                        self.next = tk.Button(self.frame_konfirmasi_listrik, text='Lanjut',width=12, border=0, anchor='center', font=('Helvetica', 16, 'bold'),
                                                                                                  bg="#ffa41c", fg='black',activebackground="#ffa41c",
                                                                             activeforeground="black",command=next_transaksi_l)
                                        self.next.place(x=310, y=240)
                                else:
                                    self.frame_9 = tk.Frame(self.mains)
                                    self.frame_9.place(x=520, y=270)

                                    bg3_image = Image.open("images\Frame 26.png")
                                    resize_image = bg3_image.resize((219, 227))
                                    self.photo2 = ImageTk.PhotoImage(resize_image)

                                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                    self.lbl_frame.image = self.photo2
                                    self.lbl_frame.pack()

                                    def oouutt():
                                        self.frame_9.destroy()

                                    self.outbut9 = tk.Button(self.frame_9,
                                                             font=('Helvetica'),
                                                             text="x",
                                                             fg="#ffffff",
                                                             bg="#FDCB7F",
                                                             border=0,
                                                             activebackground="#FDCB7F",
                                                             activeforeground="#ffffff",
                                                             cursor="hand2",
                                                             width=3,
                                                             command=oouutt)
                                    self.outbut9.place(x=175, y=7)
                            else:
                                self.frame_9 = tk.Frame(self.mains)
                                self.frame_9.place(x=520, y=270)

                                bg3_image = Image.open("images\Frame 26.png")
                                resize_image = bg3_image.resize((219, 227))
                                self.photo2 = ImageTk.PhotoImage(resize_image)

                                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                                self.lbl_frame.image = self.photo2
                                self.lbl_frame.pack()

                                def oouutt():
                                    self.frame_9.destroy()

                                self.outbut9 = tk.Button(self.frame_9,
                                                         font=('Helvetica'),
                                                         text="x",
                                                         fg="#ffffff",
                                                         bg="#FDCB7F",
                                                         border=0,
                                                         activebackground="#FDCB7F",
                                                         activeforeground="#ffffff",
                                                         cursor="hand2",
                                                         width=3,
                                                         command=oouutt)
                                self.outbut9.place(x=175, y=7)
                        else:
                            self.frame_9 = tk.Frame(self.mains)
                            self.frame_9.place(x=520, y=270)

                            bg3_image = Image.open("images\Frame 48.png")
                            resize_image = bg3_image.resize((219, 227))
                            self.photo2 = ImageTk.PhotoImage(resize_image)

                            self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                            self.lbl_frame.image = self.photo2
                            self.lbl_frame.pack()

                            def oouutt():
                                self.frame_9.destroy()

                            self.outbut9 = tk.Button(self.frame_9,
                                                     font=('Helvetica'),
                                                     text="x",
                                                     fg="#ffffff",
                                                     bg="#FDCB7F",
                                                     border=0,
                                                     activebackground="#FDCB7F",
                                                     activeforeground="#ffffff",
                                                     cursor="hand2",
                                                     width=3,
                                                     command=oouutt)
                            self.outbut9.place(x=175, y=7)
                    else:
                        self.frame_9 = tk.Frame(self.mains)
                        self.frame_9.place(x=520, y=270)

                        bg3_image = Image.open("images\Frame 49.png")
                        resize_image = bg3_image.resize((219, 227))
                        self.photo2 = ImageTk.PhotoImage(resize_image)

                        self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                        self.lbl_frame.image = self.photo2
                        self.lbl_frame.pack()

                        def oouutt():
                            self.frame_9.destroy()

                        self.outbut9 = tk.Button(self.frame_9,
                                                 font=('Helvetica'),
                                                 text="x",
                                                 fg="#ffffff",
                                                 bg="#FDCB7F",
                                                 border=0,
                                                 activebackground="#FDCB7F",
                                                 activeforeground="#ffffff",
                                                 cursor="hand2",
                                                 width=3,
                                                 command=oouutt)
                        self.outbut9.place(x=175, y=7)
                else:
                    self.frame_9 = tk.Frame(self.mains)
                    self.frame_9.place(x=520, y=270)

                    bg3_image = Image.open("images\Frame 37.png")
                    resize_image = bg3_image.resize((219, 227))
                    self.photo2 = ImageTk.PhotoImage(resize_image)

                    self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                    self.lbl_frame.image = self.photo2
                    self.lbl_frame.pack()

                    def oouutt():
                        self.frame_9.destroy()

                    self.outbut9 = tk.Button(self.frame_9,
                                             font=('Helvetica'),
                                             text="x",
                                             fg="#ffffff",
                                             bg="#FDCB7F",
                                             border=0,
                                             activebackground="#FDCB7F",
                                             activeforeground="#ffffff",
                                             cursor="hand2",
                                             width=3,
                                             command=oouutt)
                    self.outbut9.place(x=175, y=7)
            else:
                self.frame_9 = tk.Frame(self.mains)
                self.frame_9.place(x=520, y=270)

                bg3_image = Image.open("images\Frame 36 (1).png")   #Michael Fahrudin (23031554139)
                resize_image = bg3_image.resize((219, 227))
                self.photo2 = ImageTk.PhotoImage(resize_image)

                self.lbl_frame = tk.Label(self.frame_9, image=self.photo2)
                self.lbl_frame.image = self.photo2
                self.lbl_frame.pack()

                def oouutt():
                    self.frame_9.destroy()

                self.outbut9 = tk.Button(self.frame_9,
                                         font=('Helvetica'),
                                         text="x",
                                         fg="#ffffff",
                                         bg="#FDCB7F",
                                         border=0,
                                         activebackground="#FDCB7F",
                                         activeforeground="#ffffff",
                                         cursor="hand2",
                                         width=3,
                                         command=oouutt)
                self.outbut9.place(x=175, y=7)

        self.frame_l = tk.Frame(self.mains)
        self.frame_l.place(x=400, y=90)
        
        bg3_image = Image.open("images\Frame 18 (2).png")  #Michael Fahrudin (23031554139)
        resize_image = bg3_image.resize((520, 620))
        self.photo2 = ImageTk.PhotoImage(resize_image)

        self.lbl_frame = tk.Label(self.frame_l, image=self.photo2)
        self.lbl_frame.image = self.photo2
        self.lbl_frame.pack()

        def nomlis(e):
            lis = self.nominal_listrik.get()
            if lis == "Nominal":
                self.nominal_listrik.delete(0,"end")
        #
        def nomlis_zoomout(e):
            nama = self.nominal_listrik.get()
            if nama == "":
                self.nominal_listrik.insert(0,"Nominal")

        def tokenlis(e):
            token = self.no_token_listrik.get()
            if token == "No. Token Listrik":
                self.no_token_listrik.delete(0,"end")
        #
        def tokenlis_zoomout(e):
            nama = self.no_token_listrik.get()
            if nama == "":
                self.no_token_listrik.insert(0,"No. Token Listrik")

        def quitL():
            self.frame_l.destroy()

        self.nominal_listrik = tk.Entry(self.frame_l,
                                font=('Helvetica', 20),
                                fg="#777777",
                                bg="white",
                                width=19,
                                border=0,)
        self.nominal_listrik.place(y=196, x=118)
        self.nominal_listrik.insert(0, "Nominal")
        self.nominal_listrik.bind('<FocusIn>', nomlis)
        self.nominal_listrik.bind('<FocusOut>', nomlis_zoomout)

        self.no_token_listrik = tk.Entry(self.frame_l,
                                     font=('Helvetica', 20),
                                     fg="#777777",
                                     bg="white",
                                     width=19,
                                     border=0
                                     )
        self.no_token_listrik.place(x=118,y=279)
        self.no_token_listrik.insert(0, "No. Token Listrik")
        self.no_token_listrik.bind('<FocusIn>', tokenlis)
        self.no_token_listrik.bind('<FocusOut>', tokenlis_zoomout)

        self.nextButt_buyListrik = tk.Button(self.frame_l,
                                          text='Lanjut',
                                          font=("Helvetica", 17, 'bold'),
                                          fg="#ffffff",
                                          bg="#FDCB7F",
                                          border=0,
                                          activebackground="#FDCB7F",
                                          activeforeground="#ffffff",
                                          cursor="hand2",
                                          width=21,
                                          command=pinL
                                          )
        self.nextButt_buyListrik.place(x=110, y=357)


        self.quit_listrik_button = tk.Button(self.frame_l,
                                               text='X',
                                               font=("Helvetica", 21, 'bold'),
                                               fg="#ffffff",
                                               bg="#FDCB7F",
                                               border=0,
                                               activebackground="#FDCB7F",
                                               activeforeground="#ffffff",
                                               cursor="hand2",
                                               width=3,
                                              command=quitL
                                               )
        self.quit_listrik_button.place(x=465, y=9)

    def show_balance(self):
        def format_angka(angka):
            locale.setlocale(locale.LC_NUMERIC, 'id_ID')
            angka_terformat = locale.format_string("%d", angka, grouping=True)
            return angka_terformat

        angka = int(self.balance)
        self.show_balance_label = tk.Label(self.mains,
                                            text=f"{format_angka(angka)} ",
                                            font=('Helvetica', 20, 'bold'),
                                            bg='white',
                                            fg="black",
                                           width=14,
                                           anchor='w'
                                            )
        self.show_balance_label.place(x=183, y=149)

    def hide_balance(self):
        self.hide_balance_label = tk.Label(self.mains,
                                           text='● ● ● ● ●',
                                           font=('Helvetica', 22),
                                           bg='white',
                                           fg="black",
                                            width=14,
                                            anchor="w"
                                            )
        self.hide_balance_label.place(x=183, y=146)

    def toggle_command(self):
        if self.click_count % 2 == 1:
            self.hide_balance()
            self.click_count += 1
        else:
            self.show_balance()
            self.click_count += 1

    def print_receipt(self, transaction_type, amount, no_resi):
        receipt= f"receipt {self.login_username}.txt"
        with open(receipt, 'a') as f:
            f.write('\n')
            f.write("\n" + "-" * 20)
            f.write(f"\nTanggal\t\t: {datetime.datetime.now()}")
            f.write(f"\nNama\t\t: {self.login_username}")
            f.write(f"\nTransaksi\t: {transaction_type}")
            f.write(f"\nNo. Resi\t: {no_resi}")
            f.write(f"\nJumlah\t\t: Rp{amount}")
            f.write(f"\nSaldo Akhir\t: Rp{self.balance}")
            f.write("\n" + "-" * 20)

    def print_receipt_for_buy_listrik(self, transaction_type, amount, results, no_resi):
        receipt= f"receipt {self.login_username}.txt"
        with open(receipt, 'a') as f:
            f.write('\n')
            f.write("\n" + "-" * 20)
            f.write(f"\nTanggal\t\t: {datetime.datetime.now()}")
            f.write(f"\nNama\t\t: {self.login_username}")
            f.write(f"\nTransaksi\t: {transaction_type}")
            f.write(f"\nNo. Resi\t: {no_resi}")
            f.write(f'\nNomer Token\t: {results}')
            f.write(f"\nJumlah\t\t: Rp{amount}")
            f.write(f"\nSaldo Akhir\t: Rp{self.balance}")
            f.write("\n" + "-" * 20)

root = Tk()
my_bsd = BankSainsData(root)
root.mainloop()
