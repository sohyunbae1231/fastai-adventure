from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from .models import User
from datetime import datetime
import time

from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from django.views.generic import View
from .models import User, Stock, Bookmark
import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import plotly
from functools import wraps
import plotly.express as px
import plotly.graph_objs as go
import datetime
from .utils import get_plot,get_bar_graph
from django.core.paginator import Paginator
from PIL import Image
import os
import numpy as np
from django.contrib.auth import login as login_a 
# ,authenticaste

from .prediction import predict, getLabels

from pathlib import Path
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage



class EmailThread(threading.Thread):
    def __init__(self, email, username):
        self.email = email
        threading.Thread.__init__(self)

    def run (self):

        user = User.objects.get(email=self.email)
        print(user)

        

        while(1): 
            
            bookmarks = Bookmark.objects.filter(user__email=self.email) 

            now = datetime.datetime.now()
            print(user.mail_alarm_time_hour)
            print(user.mail_alarm_time_minute)

            if now.hour == user.mail_alarm_time_hour and now.minute == user.mail_alarm_time_hour :
            # if now.hour == 4 and now.minute == 45 :

                title = "🔔 fastock에서 " + user.username + "님께 보내는 북마크 알림 메일이 도착했어요!"
              

                html_content = render_to_string('stock/mail_template.html', context ={'bookmarks':bookmarks, 'user':user}) # render with dynamic value
                text_content = strip_tags(html_content)
                
                # create the email, and attach the HTML version as well.
                
                msg = EmailMultiAlternatives(title, text_content,  to=[user.email])
                msg.mixed_subtype = 'related'
                msg.attach_alternative(html_content, "text/html")

                img_dir = 'stock/templates/static/logo/'
                image = 'for_mail.PNG'
                file_path = os.path.join(img_dir, image)
                with open(file_path, 'rb' ) as f:
                    img = MIMEImage(f.read())
                    img.add_header('Content-ID', '<{name}>'.format(name=image))
                    img.add_header('Content-Disposition', 'inline', filename=image)
                msg.attach(img)

                msg.send(fail_silently=False)


                # title = "stocker에서 " + user.username + "님께 보내는 북마크 알림 메일이 도착했어요!"
                # contents = '당신이 북마크했던 종목이에요!! ( 부가 설명 더 쓰기 ) ( 영어로 바꾸기 ) ' + b 
                # # to-do 남은것
                # # html 형식으로 보내주기 / 설명 적기 !! 
                # # 이미지 첨부 할까 말까 
               
                # msg = EmailMultiAlternatives(title, contents, to=[user.email])
                # # msg.content_subtype = 'html'
                # msg.send()

                time.sleep(1)
                print('스레드 한 개 작업 완료')

                return 0
            

            else :
                print(now.hour)
                print(now.minute)
                time.sleep(1)
                pass



#이렇게 하면 views.py 에 임포트 될때 딱 한번 실행 됨 
#views.py에서는 이거 실행하기 위해 임포트 하는거고 views.py 안에서 이 클래스를 사용할 일은 없고 사용 하려면 디자인을 바꿔야함 
# def send_email(subject, body, to_email): 


# 알람 성정한 user 객체 수 만큼  for문 돌리기 
alarm_users=User.objects.exclude(mail_alarm_time_hour=None)

for alarm_user in alarm_users :
    EmailThread(alarm_user.email,alarm_user.username).start()  #start()가 run메서드를 호출함

