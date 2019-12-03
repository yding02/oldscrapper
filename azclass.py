import urllib.request
import time
import base64
import hashlib
import hmac
import urllib.parse

class Azurl:
    """Class that supports creation and manipulation of amazon api requests"""
    def __init__(self, service, endpoint, uri, aws_access_key, aws_secret_key, associate_tag):
        self.endpoint = endpoint
        self.uri = uri
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.params = {"Service":service,
                       "AWSAccessKeyId":aws_access_key,
                       "AssociateTag":associate_tag}
        return

    def add_params(self, new_params):
        """Updates old param if param already exists. Otherwise adds new params.
        NEW_PARAMS are defined as a dictionary
        """
        for key in new_params.keys():
            self.params[key] = new_params[key]
        return

    def bind_timestamp(self):
        self.add_params({'Timestamp':time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        return
    
    def make_query_string(self, encoding = urllib.parse.quote):
        """Makes a query sting from the various params bound"""
        keys = list(self.params.keys())
        keys.sort()
        pairs = []
        for key in keys:
            pairs.append(encoding(key)+"="+encoding(self.params[key]))
        self.query_string = '&'.join(pairs)
        return
    
    def sign_string(self, encoding = urllib.parse.quote):
        """Signs query string from self.query_string"""
        string_to_sign = "GET\n%s\n%s\n%s" % (self.endpoint, self.uri, self.query_string)
        string_to_sign = string_to_sign.encode("ascii")
        b = bytearray()
        b.extend(map(ord, self.aws_secret_key))
        self.signature = encoding(base64.b64encode(hmac.new(b, msg=string_to_sign, \
                                     digestmod=hashlib.sha256).digest()).decode())
        return

    def make_request_url(self):
        """Makes a request url from self.query_string and self.signiture"""
        self.request_url = "http://{}{}?{}&Signature={}".format(self.endpoint, self.uri, self.query_string, self.signature)
        return

    def make_url(self):
        """Does many steps at once from binding params directly to url"""
        self.bind_timestamp()
        self.make_query_string()
        self.sign_string()
        self.make_request_url()
        return

    def get_request_url(self):
        """Returns url to search query"""
        return self.request_url

    def fetch_url(self):
        """Fectches the page from self.request_url"""
        req = urllib.request.Request(self.request_url)
        tries = 3
        while tries > 0:
            try:
                time.sleep(1)
                response = urllib.request.urlopen(req)
                break
            except urllib.request.HTTPError as e:
                print(e.code)
                tries -= 1
                #delay as required for web requests
                time.sleep(3*(3-tries))
        if tries == 0:
            return False
        return response
