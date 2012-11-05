import imaplib
import os , time, logging, re, sys
import email
from flask import Flask, session, request, redirect, url_for, render_template, jsonify, Response
import socket
import chardet
from flask.ext.cache import Cache



app = Flask(__name__, static_url_path='')
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app, config={'CACHE_TYPE': 'simple'})

Flask.secret_key = os.environ.get('FLASK_SESSION_KEY', os.environ.get('SECRET_KEY', 'test-key-please-ignore'))

logging.basicConfig( 
    stream=sys.stdout, 
    level=logging.DEBUG, 
    format='"%(asctime)s %(levelname)8s %(name)s - %(message)s"', 
    datefmt='%H:%M:%S' 
) 

PORT = int(os.environ.get('PORT', 5000))
if 'PORT' in os.environ:
    HOSTNAME = 'fwol.in'
    HOST = 'fwol.in'
else:
    HOSTNAME = 'localhost'
    HOST = 'localhost:5000'


app.mail = imaplib.IMAP4_SSL('imap.gmail.com')
app.mail.login(os.environ.get('ARCHIVEEMAIL') or "empty", os.environ.get('ARCHIVEPASSWORD') or "secret")




# Out: list of "folders" aka labels in gmail.
app.mail.select("inbox") # connect to inbox.


@app.route('/')
def search():
    query = request.args.get('query', False,type=str)
    onCampus = isAtOlin(request)
    logging.debug("Is At Olin: %s" % onCampus)
    logging.debug("Query:%s" % query)
    emailIds = []
    if query:
        t1 = time.time()
        emailIds = getSearchGenerator(query)
        logging.debug('Querying %s emails took %0.3f ms' % (len(emailIds), (time.time()-t1)*1000.0))

    return render_template('search.html',emails=getEmailBatch(emailIds[:50]), shouldServe=onCampus)


@app.route('/search')
def apiQuery():
    query = request.args.get('query', False,type=str)
    if query:
        emailIds = getSearchGenerator(query, label="")
        return jsonify(emails=[getEmail(uid) for uid in emailIds[:10]])
    else:
        return jsonify({"error":"No query parameter set"}),400 #bad request


@app.route('/mu-c9d98459-e81972b2-54d297df-5e25108c')
def blitzAuthorize():
    return '42'

def isAtOlin(req):
    host,_,_ = socket.gethostbyaddr(request.remote_addr)
    return  'olin' in host

def getEmail(uid):
    typ, data = app.mail.fetch(uid, '(RFC822)')
    msg = email.message_from_string(data[0][1]) 
    return {"body" : re.sub("^(\s*\r\n){2,}",'\r\n',getBody(msg)).split('\r\n'),
            "subject" : msg["subject"],
            "date" : msg.get('date')
            }


def getSlices(data):
    for i in range(len(data)/2):
        yield data[i*2:(i*2) + 2]

def getEmailBatch(uids):
    res = []
    queryString = ','.join([numail for numail in uids])
    typ, data = app.mail.fetch(queryString, '(RFC822)')
    for d in getSlices(data):
        msg = email.message_from_string(d[0][1]) 
        res.append({"body" : re.sub("^(\s*\r\n){2,}",'\r\n',getBody(msg)).split('\r\n'),
                "subject" : msg["subject"],
                "date" : msg.get('date')
                })      
    return reversed(res)
def getSlices(data):
    for i in range(len(data)/2):
        yield data[i*2:(i*2) + 2]

def getSlices(data):
    for i in range(len(data)/2):
        yield data[i*2:(i*2) + 2]

def getBody(msg):
    res = ''
    for part in msg.walk():
        if part.get_content_type() == "text/plain": #we don't want the HTML, or attachments
            if part.get_content_charset() is None:
                charset = chardet.detect(str(part))['encoding']
            else:
                charset = part.get_content_charset()
            try:
                res += unicode(part.get_payload(decode=True) or '',str(charset),"ignore")
            except Exception as e:
                logging.error("Decoding error: %s original={%s}"%(e, part.get_payload(decode=True)))
                continue
    return res.replace("-------------- next part --------------\r\nSkipped content of type text/html","")

@cache.memoize()
def getSearchGenerator(query):
    try:
        typ, data = app.mail.search('utf8', '(X-GM-RAW "%s")'% query)
        return [r for r in reversed(data[0].split())] #Google gives them in reverse date order...
    except imaplib.IMAP4.abort as e:
        logging.error(e)
        app.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        app.mail.login(os.environ.get('ARCHIVEEMAIL') or "empty", os.environ.get('ARCHIVEPASSWORD') or "secret")
        app.mail.select("inbox") # connect to inbox.
        return getSearchGenerator(query)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    app.run(host=HOSTNAME, port=PORT)
