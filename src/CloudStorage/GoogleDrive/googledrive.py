#! /usr/bin/python

import os
import sys
import json
import base64
import urllib
import urllib2
import httplib
import argparse
from getpass import getpass
from mimetypes import guess_type
from urlparse import urlparse, parse_qs
from datetime import datetime, timedelta


KEYS_FILENAME = 'keys.txt'


class GoogleDriveClient(object):
    def http(self, act, url, data="", hd={}):
        host = urlparse(url)[1]
        conn = httplib.HTTPSConnection(host)
        conn.request(act, url, data, hd)
        res = conn.getresponse()
        ret = res.read()
        #print ret
        #print res.status
        #print res.reason
        #print res.getheaders()
        return ret

    def check_auth(self, infn):
        if not os.path.isfile(infn):
            print >> sys.stderr, "Can not find", infn, "you have goto"
            print >> sys.stderr, "https://code.google.com/apis/console/"
            print >> sys.stderr, "register"
            print >> sys.stderr, "Please check README.md for detail"
            sys.exit(1)
        try:
            self.token = t = json.load(open(infn))
        except Exception, e:
            print >> sys.stderr, e
            t = {}
        if 'access_token' not in t or 'refresh_token' not in t:
            print >> sys.stderr, "you have run '--auth ", infn
            print >> sys.stderr, "' to get auth before any operation"
            sys.exit(1)
        self.web = self.token['web']
        edt = datetime.strptime(self.token['before_this_time'],
                                "%Y-%m-%d %H:%M:%S")
        if edt < datetime.today():
            self.refresh_token()
            json.dump(open(infn, 'w'))

    def _update_token(self, ret):
        dat = json.loads(ret)
        for k, v in dat:
            self.token[k] = v
        edt = datetime.today() + timedelta(seconds=self.token['expires_in']/2)
        self.token['before_this_time'] = etd.strftime("%F %T")

    def refresh_token(self):
        url = "https://accounts.google.com/o/oauth2/token"
        data = urllib.urlencode({
                                "refresh_token": self.token['refresh_token'],
                                "client_id": self.web['client_id'],
                                "client_secret": self.web['client_secret'],
                                "grant_type": "refresh_token",
                                })
        ret = self.http("POST", url, data,
                        {"Content-Type": "application/x-www-form-urlencoded"})
        self._update_token(ret)

    def acquire_token(self, infn):
        self.token = json.load(open(infn))
        pa = {
            "response_type": "code",
            "client_id": t['web']['client_id'],
            "redirect_uri": "http://localhost:8080/oauth",
            "state": "QunPin",
            "access_type": "offline",
            "scope": ("https://www.googleapis.com/auth/drive "
                      "https://www.googleapis.com/auth/userinfo.email "
                      "https://www.googleapis.com/auth/userinfo.profile")
            }
        print "Visit this url, input the code:"
        print "https://accounts.google.com/o/oauth2/auth?" + urlencode(pa)
        code = raw_input("code:")
        web = self.token['web']
        url = "https://accounts.google.com/o/oauth2/token"
        data = urllib.urlencode({
                                "code": code,
                                "client_id": web['client_id'],
                                "client_secret": web['client_secret'],
                                "redirect_uri": "http://localhost:8080/oauth",
                                "grant_type": "authorization_code",
                                })
        ret = self.http("POST", url, data,
                        {"Content-Type": "application/x-www-form-urlencoded"})
        self._update_token(ret)

    def query(self, word):
        res = self.get("https://one.ubuntu.com/api/file_storage/"
                       "v1/~/Ubuntu%20One?include_children=true")
        data = json.loads(res)
        #print data['children'][0]['content_path']
        for child in data['children']:
            if child.get('kind') != 'file':
                continue
            fn = child.get('content_path')
            if not fn:
                continue
            fn = os.path.basename(fn)
            if word and word in fn:
                print fn

    def delete(self, filename):
        name = os.path.basename(filename)
        url = ("https://one.ubuntu.com/api/file_storage/v1"
               "/~/Ubuntu%20One/" + urllib.quote(name))
        self.put("DELETE", url)

    def upload(self, filename):
        name = os.path.basename(filename)
        url = ("https://files.one.ubuntu.com/content"
               "/~/Ubuntu%20One/" + urllib.quote(name))
        mime = guess_type(name)
        if not mime or not mime[0]:
            mime = "text/plain"
        self.put("PUT", url, mime, open(filename))


def main():
    parser = argparse.ArgumentParser(description="Use command line to "
                                                 "control GoogleDrive")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--auth", "-A", help="Authorise by google drive user")
    group.add_argument("--query", "-Q", help="Query file by key word")
    group.add_argument("--upload", "-U", help="Upload a file")
    group.add_argument("--delete", "-D", help="Delete a file")

    args = parser.parse_args()
    clt = GoogleDriveClient()

    if args.auth:
        clt.acquire_token(KEYS_FILENAME)
        sys.exit(0)

    if args.upload or args.delete or args.query:
        clt.check_auth(KEYS_FILENAME)
    else:
        parser.print_help()
        sys.exit(1)

    if args.upload:
        clt.upload(args.upload)
    elif args.delete:
        clt.delete(args.delete)
    elif args.query:
        clt.query(args.query)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
