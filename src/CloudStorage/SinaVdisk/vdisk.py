import argparse
import hmac
import hashlib
import time
import logging
import sys

## easy_install requests
## or we should add https://github.com/kennethreitz/requests.git as a submodule.
import requests

App_Key="2000904490"
App_Secret="0e4514df35df979dd1e58681319246e7"

class vdisk_api():
    def __init__(self,account,password,app_type=None):
        self.account=account
        self.password=password
        self.token=''
        self.app_type=app_type
        
    def get_token(self):
        url="http://openapi.vdisk.me/?m=auth&a=get_token"
        t=int(time.time())
        if self.app_type:
            self.app_type="local"
        signature=hmac.new(App_Secret,"account="+self.account+"&appkey="+App_Key+"&password="+
                           self.password+"&time="+repr(t),hashlib.sha256).hexdigest()
        data=dict(account=self.account,
                  password=self.password,
                  appkey=App_Key,time=t,
                  signature=signature,
                  app_type=self.app_type)
        response=requests.post(url,data1)
        if response.json['err_code']==0:
            self.token=response.json['token']
        else:
            logging.error(response.json['err_msg'])

    def keep(self):
        
        






parser=argparse.ArgumentParser(description="Use command line to control vdisk")
group=parser.add_mutually_exclusive_group()
group.add_argument("--upload","-U",help="upload a file")
group.add_argument("--delete","-D",help="delete a file")
group.add_argument("--query","-Q",help="query file by key word")

args=parser.parse_args()

if args.upload:
    print args.upload
elif args.delete:
    print args.delete
elif args.query:
    print args.query
else:
    pass
