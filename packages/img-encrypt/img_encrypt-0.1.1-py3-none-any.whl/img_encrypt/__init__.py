def keymaker(password):
        pas=bytearray(bytes(password.encode()))
        key=0
        for i in pas:
                key+=i
        return key
def image_data(path):
        with open(path,'rb') as f:
                data=f.read()
        return data
def dataextra(data,key):
        if ((len(data)-(len(data)%key))//key)%2==0:
                 data_extra=data[-(len(data)%key):]
                 data=data[:-(len(data)%key)]
        else:
                 data_extra=data[-((len(data)%key)+key):]
                 data=data[:-((len(data)%key)+key)]
        return data_extra,data
def convert(data,key=100):
         work_str=b''
         for i in range(1,len(data),2):
                work_str+=data[((i+1)-1)*key:(i+1)*key]+data[(i-1)*key:i*key]
         return work_str
def img_maker(data,extra,outputpath):
        data=data+extra
        with open(outputpath,'wb') as f:
                f.write(data)
#CONVERTER IS FINAL PROGRAM TO CONVERT ENC TO DECRYPT AND DECRYPT To ENCRYPT
def converter(path,password,outputpath):
      key=keymaker(password)
      data_extra=dataextra(image_data(path),key)
      img_maker(convert(data_extra[1],key=key),data_extra[0],outputpath)
      with open('password.txt','a') as f:
              f.write(password+'\n')
      return 'Converted */'+outputpath
#img_maker(img_enc(image_data('2.jpg'),key=keymaker('amit ydav')))
