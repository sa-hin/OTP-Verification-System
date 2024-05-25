
import PIL.Image
import PIL.ImageTk
import random 
import smtplib 
import re
from email.message import EmailMessage
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


class OTPVerifier(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x500+200+80") 
        self.title("OTP Verifcation") 
        self.configure(bg="")
        self.resizable(False,False) 

        self.attempts_left = 3
        self.create_design()
        
    def create_design(self):
        self.canvas = Canvas(self, width=1000, height=500)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

        
        # Load image
        img = PIL.Image.open(r"C:\OTP.verification.project\use_image.jpg")
        img = img.resize((1000, 700), resample=PIL.Image.LANCZOS)  # Resize the image if needed
        self.img = PIL.ImageTk.PhotoImage(img) 
        # Add image to canvas
        
        self.canvas.create_image(500, 350, image=self.img, anchor=CENTER)
        self.canvas.create_text(500, 100, text="OTP Verification System", font=("Helvetica", 30, "bold"), fill="#4682B4")
        

        self.otp = ""  
        self.server = ""
        self.from_mail = 'your_email_address' 
        self.to_mail = ""
        self.msg = ""
        

        self.Labels()
        self.Entry()
        self.Buttons() 
        self.attempts_label = Label(self, text="", font=("Helvetica", 24), bg="#FFFACD")
        self.attempts_label.place(relx=0.5, rely=0.7, anchor=CENTER)

    def Labels(self):
        self.label = Label(self,text="Enter your email", font=("Helvetica", 24, "bold"), fg="#4682B4")
        self.label.place(relx= 0.5, rely=0.4, anchor= CENTER)
       

    def Entry(self):
        self.email_entry = Entry(self, font=("Helvetica", 16), highlightcolor= "grey", highlightthickness= 2)    
        self.email_entry.place(relx=0.5, rely=0.5, anchor=CENTER)
       

    def Buttons(self): 
        self.submit_button = Button(self, text="Send OTP", command =self.send_otp, font=("Helvetica", 16), bg="grey", fg="white", activebackground="lightblue")   
        self.submit_button.place(relx=0.5, rely=0.6, anchor=CENTER)
          


    def send_otp(self):
        
        self.to_mail = self.email_entry.get()
        # Check if the email entry field is empty
        if not self.to_mail:
            messagebox.showerror("Error", "Please enter your Email.")
            return 
        
        # Validate email format using regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.to_mail):
            messagebox.showerror("Error", "Please enter a valid Gmail address.")
            return
        
        self.otp = ""
        for i in range(6):
             self.otp += str(random.randint(0,9))
        
        self.msg = EmailMessage()
        self.msg['Subject'] = 'OTP Verification'
        self.msg['From'] = self.from_mail 
        self.msg['To'] = self.to_mail 
        self.msg.set_content('Your OTP is: ' + self.otp)

        # Connect to SMTP server and send email
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.from_mail, 'your_Gmail_password') 
        self.server.send_message(self.msg)
        
        messagebox.showinfo("Email Sent", "The OTP has been sent to your email")
        
        for _ in range(3):
            input_otp = simpledialog.askstring("OTP Verification", "Enter OTP:")
            if input_otp == self.otp:
               messagebox.showinfo("OTP Verification", "OTP Verified")
               break
            else:
              self.attempts_left -= 1
              if self.attempts_left > 0:
                 messagebox.showerror("Invalid OTP", f"Invalid OTP! Attempts left: {self.attempts_left}")
              else:
                 messagebox.showerror("OTP Verification", "Maximum attempts reached. Please try again later.")
                 self.server.quit()
                 return
        else:
          messagebox.showerror("OTP Verification", "Maximum attempts reached. Please try again later.")
          self.server.quit()


if __name__ == "__main__":
    window = OTPVerifier()
    window.mainloop() 



