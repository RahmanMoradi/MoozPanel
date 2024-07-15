from requests import post
from random import choice
from string import ascii_lowercase, hexdigits, ascii_letters, digits
from json import loads
from datetime import datetime, timedelta
from . import InvalidUsernameOrPassword, CantAddClient, UndefinedProtocol
from urllib.parse import urlparse

class xui:
    def __init__(
        self,
        address,
        username = 'admin',
        password = 'admin',
        cookie = None
    ):
        self.address = urlparse(address).netloc.split(':')[0]
        self.username = username
        self.password = password
        self.cookie = cookie
        self.full_address = address[:-1:] if address[-1] == '/' else address
        if isinstance(cookie, str):
            self.cookie = {'session': cookie}
        if not self.cookie:
            self.cookie = self.login()

    def Calculate(self, GB):
        return str(GB*1024**3)

    def GetExpireTime(self, day):
        expire_time = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') + timedelta(days=day)
        return str(int(expire_time.timestamp()))

    def login(self):
        username_password = {
            'username': self.username,
            'password': self.password
        }
        cookies = post(self.full_address+'/login', data=username_password).cookies.get_dict()
        if not cookies:
            raise InvalidUsernameOrPassword('invalid username or password')
        return cookies

    def UpdateCookie(self, NewCookie):
        if isinstance(NewCookie, str):
            self.cookie = {'session': NewCookie}
        else:
            self.cookie = NewCookie
        return True

    @property
    def GetCookie(self):
        return self.cookie

    def RandomID(self):
        information =  post(self.full_address+'/panel/inbound/list', cookies=self.cookie).json()
        ID = '-'.join([''.join([choice(hexdigits[:-6:]) for _ in range(i)]) for i in [8,4,4,4,12]])
        if ID in information:
            return self.RandomID
        return ID

    def GetInboundInformation(self, InboundID : int) -> dict:
        page = post(self.full_address+'/panel/inbound/list', cookies=self.cookie).json()
        for obj in page['obj']:
            if obj['id'] == int(InboundID):
                return obj
        return False

    def EncodeTag(self, Tag):
        return ''.join(f'%{ord(i):x}' if not i in ascii_letters+digits else i for i in Tag)

    def CreateVless(self, ClientID, Address, Port, Tag, Network, Security):
        EncodedTag = self.EncodeTag(Tag)
        return f'vless://{ClientID}@{Address}:{Port}?type={Network}&security={Security}#{EncodedTag}'

    def AddClient(self, InboundID, Days, GB, UserID = RandomID, ConfigName = 'MoozPanel'):
        if not isinstance(UserID, str):
            UserID = UserID(self)
        settings = {
            'id': InboundID,
            'settings': '{"clients": [{ "id": "'+UserID+'", "flow": "", "email": "'+UserID+'", "limitIp": 0, "totalGB": '+self.Calculate(int(GB))+', "expiryTime": '+self.GetExpireTime(int(Days))+', "enable": true, "tgId": "", "subId": "'+''.join(choice(ascii_lowercase) for _ in range(16))+'", "reset": 0 }]}'
        }
        if post(self.full_address+'/panel/inbound/addClient', data=settings, cookies=self.cookie).json()['success']:
            info = self.GetInboundInformation(InboundID)
            streamSettings = loads(info['streamSettings'])
            Network = streamSettings['network']
            Secutiy = streamSettings['security']
            if info['protocol'] == 'vless':
                return self.CreateVless(UserID, self.address, info['port'], ConfigName, Network, Secutiy)
            raise UnfefinedProtocol('It will be added in other versions')
        raise CantAddClient('An error occurred')