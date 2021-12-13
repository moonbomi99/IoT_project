from tkinter import *
from tkinter import messagebox
import picamera
import RPi.GPIO as GPIO 
from PIL import Image
import time
import datetime

SERVO_PIN = 27
wled_pin=21
rled_pin = 4
gled_pin=25
button_pin=15
frame=Tk()

frame.title("keypad")
frame.resizable(False,False)
inputpassword=""
password="0419"
dochange=False
catchcamera=False
isopen=False
count=0
servo_on=False
secret=""

GPIO.setwarnings(False) 
# GPIO핀의 번호 모드 설정
GPIO.setmode(GPIO.BCM) 
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(rled_pin, GPIO.OUT)
GPIO.output(rled_pin,0)
GPIO.setup(gled_pin, GPIO.OUT)
GPIO.output(gled_pin,0)
GPIO.setup(wled_pin, GPIO.OUT)
GPIO.output(wled_pin,0)
GPIO.setup(17, GPIO.OUT)
# PWM 인스턴스 p를 만들고  GPIO 18번을 PWM 핀으로 설정, 주파수  = 100Hz
p = GPIO.PWM(17, 100) 
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN,50)
# PWM 듀티비 0 으로 시작 


Frq = [262,131]
Frq2=[252,330,392]
Frq3=[392,330,252]
speed = 0.2

servo.start(0)
servo.ChangeDutyCycle(7.5)
#time.sleep(1)

def numberclick(number):
    global secret
    global inputpassword
    # p.start(10)
                
    # p.ChangeFrequency(196)    #주파수를 fr로 변경
    # time.sleep(speed)       #speed 초만큼 딜레이 (0.5s)
    # p.stop()
    
    try:
        if len(inputpassword)<4:
            inputpassword=inputpassword+number
            secret=secret+"*"
            
        else:
            inputpassword=""
            secret=""
        input.config(text=secret)
        #input.config(text=inputpassword)
    
    except:
        print("numberclick error")

def starclick():
    global secret
    global catchcamera
    global password
    global inputpassword
    global dochange
    global count
    global isopen
    global File

    try:
        secret=""
        if isopen==True:
            if dochange==True:
                if len(inputpassword)==4:
                    password=inputpassword
                    status.config(text="비밀번호 변경 완료")
                    dochange=False
                else:
                    status.config(text="4자리로 입력")

            else:
                count=0
                status.config(text="열림")
                input.config(text="")
                inputpassword=""
        else:
            if inputpassword==password:
                count=0
                p.start(10)
                for fr in Frq2:
                    p.ChangeFrequency(fr)    #주파수를 fr로 변경
                    time.sleep(speed)       #speed 초만큼 딜레이 (0.5s)
                p.stop()
                GPIO.output(rled_pin,0)
                GPIO.output(gled_pin,1)
                GPIO.output(wled_pin,1)
                servo.start(0)
                changebtn.grid(row=6,column=0,columnspan=3)
                photobtn.grid(row=7,column=0,columnspan=3)
                status.config(text="열림")
                input.config(text="")
                print("correct")
                servo.ChangeDutyCycle(2.5)
                isopen=True
                now=datetime.datetime.now()
                File=open("open.txt","a")
                print(now,file=File)
                File.close()
                
            else:
                count=count+1
                status.config(text=str(count)+"번 에러")
                if count==1:
                    GPIO.output(rled_pin,1)
                    
                elif count==2: 
                    
                    p.start(10)
                    for fr in Frq:
                        p.ChangeFrequency(fr)    #주파수를 fr로 변경
                        time.sleep(speed)       #speed 초만큼 딜레이 (0.5s)
                    p.stop()
                            
                

                elif count==3: # 그 이후꺼도 잊지말자
                    
                    messagebox.showinfo("error","3번 에러\n카메라 촬영")
                    with picamera.PiCamera() as camera: 
                        
                        camera.resolution = (640, 480)
                        camera.start_preview()
                        time.sleep(1)
                        camera.capture('catch.jpg')
                        camera.stop_preview()
                        catchcamera=True
                    messagebox.showinfo("error","10초 뒤 다시 실행하시오")
                    time.sleep(10)
                    GPIO.output(rled_pin,0)
                    input.config(text="")
                    status.config(text="4자리 비밀번호 입력")
                    inputpassword=""
                
                if count>=3:
                    count=0
                
        input.config(text="")
        inputpassword=""
    except:
        print("starclickerror")

def close():
    global isopen
    global count
    global catchcamera

    try:
        GPIO.output(rled_pin,0)
        GPIO.output(gled_pin,0)
        GPIO.output(wled_pin,0)
        servo.start(0)
        servo.ChangeDutyCycle(7.5)
        if isopen==True:
            p.start(10)
            for fr in Frq3:
                p.ChangeFrequency(fr)    #주파수를 fr로 변경
                time.sleep(speed)       #speed 초만큼 딜레이 (0.5s)
            p.stop()
            status.config(text="잠김")
            changebtn.grid_remove()
            photobtn.grid_remove()
            count=0
            catchcamera=False
        isopen=False

    except:
        print("closeerror")

def button_callback(channel):
    global inputpassword
    global password
    global secret
    global count
    try:
        if inputpassword=='2580':
            password='0000'
            status.config(text="비밀번호 초기화")
            input.config(text="")
            inputpassword=""
            for i in range(3):
                GPIO.output(rled_pin,1)    # LED ON
                time.sleep(0.5)   
                GPIO.output(rled_pin,0)    # LED OFF
                time.sleep(0.5)   
            status.config(text="4자리 비밀번호 입력")
            input.config(text="")
            inputpassword=""
            secret=""
            count=0
    except:
        print("buttoncallback error")

def passwordchange():
    global dochange
    global inputpassword
    try:
        status.config(text="4자리 비밀번호 입력")
        input.config(text="")
        inputpassword=""
        print("passwordchange")
        dochange=True
    except:
        print("passwordchange error")
    


def showphoto():
    global catchcamera
    global File

    try:
        File=open("open.txt","r")
        lines=File.readline()
        File.close()
        if catchcamera==True:
            im=Image.open("/home/pi/bomi/project/catch.jpg")
            im.show()
            print("showphoto")
        else:
            status.config(text="침입자가 없습니다")
    
    except:
        print("showphoto error")


GPIO.add_event_detect(button_pin,GPIO.RISING,callback=button_callback, bouncetime=300) 

title=Label(frame,text="비밀번호")
title.grid(row=0,column=0)

input=Label(frame,width=12,background='white')
input.grid(row=0,column=1,columnspan=2,pady=10,padx=3)

status=Label(frame,text="4자리 비밀번호 입력")
status.grid(row=1,column=0,columnspan=3)

btn1=Button(frame,width=3,height=2,text="1",command=lambda:numberclick("1"))
btn2=Button(frame,width=3,height=2,text="2",command=lambda:numberclick("2"))
btn3=Button(frame,width=3,height=2,text="3",command=lambda:numberclick("3"))

btn1.grid(row=2,column=0,sticky=N+E+W+S)
btn2.grid(row=2,column=1,sticky=N+E+W+S)
btn3.grid(row=2,column=2,sticky=N+E+W+S)

btn4=Button(frame,width=3,height=2,text="4",command=lambda:numberclick("4"))
btn5=Button(frame,width=3,height=2,text="5",command=lambda:numberclick("5"))
btn6=Button(frame,width=3,height=2,text="6",command=lambda:numberclick("6"))

btn4.grid(row=3,column=0,sticky=N+E+W+S)
btn5.grid(row=3,column=1,sticky=N+E+W+S)
btn6.grid(row=3,column=2,sticky=N+E+W+S)

btn7=Button(frame,width=3,height=2,text="7",command=lambda:numberclick("7"))
btn8=Button(frame,width=3,height=2,text="8",command=lambda:numberclick("8"))
btn9=Button(frame,width=3,height=2,text="9",command=lambda:numberclick("9"))

btn7.grid(row=4,column=0,sticky=N+E+W+S)
btn8.grid(row=4,column=1,sticky=N+E+W+S)
btn9.grid(row=4,column=2,sticky=N+E+W+S)

btnsign=Button(frame,width=3,height=2,text="*",command=starclick)
btn0=Button(frame,width=3,height=2,text="0",command=lambda:numberclick("0"))
btnsign2=Button(frame,width=3,height=2,text="#",command=close)


btnsign.grid(row=5,column=0,sticky=N+E+W+S)
btn0.grid(row=5,column=1,sticky=N+E+W+S)
btnsign2.grid(row=5,column=2,sticky=N+E+W+S)

changebtn=Button(frame,width=17,height=2,text="비밀번호 변경",command=passwordchange)
photobtn=Button(frame,width=17,height=2,text="침입자 확인",bg='red',command=showphoto)



frame.mainloop()