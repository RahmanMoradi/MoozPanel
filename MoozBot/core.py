#Imports...
import sqlite3
from .errors import UnfefinedProtocol, CantAddClient

#Database...
class database() :
    #Lets Code...
    def __init__(self , name) -> None:
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

    def MakeDB(self, tables) -> None:
        for i in tables :
            self.cursor.execute(i)
            self.conn.commit()

    def ChangeValue(self, Table , Val , NewVal , Condition , ConVal) -> True:
        query = f'UPDATE "{Table}" SET "{Val}" = "{NewVal}" WHERE "{Condition}" = "{ConVal}"'
        self.cursor.execute(query)
        return True

    def GetSome(self, table,where,value) -> list:
        #query = f'SELECT * FROM (?) WHERE (?) = (?)'
        query = f'SELECT * FROM {table} WHERE {where} = ?'
        self.cursor.execute(query , (value,))
        res = self.cursor.fetchall()
        return res
    
    def GetAdmins(self) -> list:
        query = f'SELECT USERID FROM USERS WHERE IsAdmin = 1'
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        res = [int(i[0]) for i in res]
        return res
    @property
    def GetUsers(self) -> list:
        query = 'SELECT * FROM USERS'
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def GetUser(self, UserId) -> bool | list:
        query = f'SELECT * FROM USERS WHERE USERID = ?'
        self.cursor.execute(query,(UserId,))
        res = self.cursor.fetchall()
        if len(res) == 0 :
            return False
        else :
            return res[0]

    def MakeUser(self, UserId , Step , Coin , IsAdmin , IsBlocked) -> bool | None:
        UT = self.GetUser(UserId)
        if UT == False :
            query = f'INSERT INTO USERS (USERID , STEP , COIN , ISADMIN , IsBlocked) VALUES (? , ? , ? , ? , ?)'
            self.cursor.execute(query , (UserId,Step,Coin,IsAdmin,IsBlocked,))
            self.conn.commit()
            return True
        else :
            query = f'UPDATE USERS SET USERID = "{UserId}", STEP  = "{Step}" , COIN = "{Coin}" , ISADMIN = "{IsAdmin}" , ISBLOCKED = "{IsBlocked}" WHERE USERID = "{UserId}"'
            self.cursor.execute(query)
            self.conn.commit()

    @property
    def GetSettings(self) -> list:
        query = f'SELECT * FROM SETTINGS'
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def GetSetting(self, Name) -> list:
        query = f'SELECT * FROM SETTINGS WHERE NAME = ?'
        self.cursor.execute(query , (Name,))
        res = self.cursor.fetchall()
        return res[0][1]

    def WriteSettings(self, Name , Value) -> bool | None:
        ST = self.GetSome('SETTINGS','NAME',Name)
        if len(ST) == 0 :
            query = f'INSERT INTO SETTINGS (NAME , VALUE) VALUES (? , ?)'
            self.cursor.execute(query , (Name,Value))
            self.conn.commit()
            return True
        else :
            query = f'UPDATE SETTINGS SET NAME = "{Name}", VALUE  = "{Value}" WHERE NAME = "{Name}"'
            self.cursor.execute(query)
            self.conn.commit()
    
    @property
    def GetPlans(self) -> list:
        query = f'SELECT * FROM PLANS'
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def GetPlan(self, Id) -> list:
        query = f'SELECT * FROM PLANS WHERE ID = ?'
        self.cursor.execute(query,(Id,))
        res = self.cursor.fetchall()
        return res[0]

    def GetPlanM(self, Time) -> list:
        query = f'SELECT * FROM PLANS WHERE TIME = ?'
        self.cursor.execute(query,(Time,))
        res = self.cursor.fetchall()
        return res
    
    def WritePlans(self, Id, Name , Amount , Price , Time) -> bool | None:
        ST = self.GetSome('PLANS','ID',Id)
        if len(ST) == 0 :
            query = f'INSERT INTO PLANS (Id , NAME , AMOUNT , PRICE , TIME) VALUES (? , ? , ? , ? , ?)'
            self.cursor.execute(query ,(Id,Name , Amount , Price , Time ,))
            self.conn.commit()
            return True
        elif len(ST) == 1 :
            query = f'UPDATE PLANS SET ID = "{Id}" , NAME = "{Name}", AMOUNT  = "{Amount}" , PRICE = "{Price}" , TIME = "{Time}" WHERE ID = "{Id}"'
            self.cursor.execute(query)
            self.conn.commit()
        else :
            return False

    @property
    def GetOrders(self) -> list:
        query = 'SELECT * FROM ORDERS'
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def GetOrder(self, Id) -> bool | list:
        query = f'SELECT * FROM ORDERS WHERE ID = ?'
        self.cursor.execute(query,(Id,))
        res = self.cursor.fetchall()
        if len(res) == 0 :
            return False
        else :
            return res[0]

    def WriteOrders(self, Id , User , Plan , Status) -> bool | None:
        ST = self.GetSome('ORDERS','ID',Id)
        if len(ST) == 0 :
            query = f'INSERT INTO ORDERS (ID , USER , PLAN , STATUS) VALUES (? , ? , ? , ?)'
            self.cursor.execute(query , (Id , User , Plan , Status))
            self.conn.commit()
            return True
        elif len(ST) == 1 :
            query = f'UPDATE ORDERS SET ID = "{Id}", USER  = "{User}" , PLAN = "{Plan}" , STATUS = "{Status}" WHERE ID = "{Id}"'
            self.cursor.execute(query)
            self.conn.commit()
        else :
            return False

    @property
    def GetMonths(self) -> list:
        query = 'SELECT * FROM MONTHS'
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res
 
    def GetMonth(self, Id) -> list:
        query = 'SELECT * FROM MONTHS  WHERE ID = ?'
        self.cursor.execute(query,(Id,))
        res = self.cursor.fetchall()
        return res[0]
    
    def WriteMonths(self, Id , Name , Days) -> bool | None:
        ST = self.GetSome('MONTHS','ID',Id)
        if len(ST) == 0 :
            query = f'INSERT INTO MONTHS (ID , NAME , DAYS ) VALUES (? , ? , ?)'
            self.cursor.execute(query , (Id , Name , Days))
            self.conn.commit()
            return True
        elif len(ST) == 1 :
            query = f'UPDATE MONTHS SET ID = "{Id}", NAME  = "{Name}" , DAYS = "{Days}" WHERE ID = "{Id}"'
            self.cursor.execute(query)
            self.conn.commit()
        else :
            return False
    

    @property
    def GetServers(self) -> list:
        query = 'SELECT * FROM SERVERS'
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def GetServer(self, Id) -> bool | list:
        query = f'SELECT * FROM SERVERS WHERE ID = ?'
        self.cursor.execute(query,(Id,))
        res = self.cursor.fetchall()
        if len(res) == 0 :
            return False
        else :
            return res[0]


    def WriteServers(self, Id , Ip , Port , UserName , Password , Name , PanelUrl , Status) -> bool | None:
        ST = self.GetSome('SERVERS','ID',Id)
        if len(ST) == 0 :
            query = f'INSERT INTO SERVERS (ID , IP , PORT , USERNAME , PASSWORD , NAME , PANELURL , STATUS) VALUES (? , ? , ? , ? , ? , ? , ? , ? )'
            self.cursor.execute(query , (Id , Ip , Port , UserName , Password , Name , PanelUrl , Status))
            self.conn.commit()
            return True
        elif len(ST) == 1 :
            query = f'UPDATE SERVERS SET ID = "{Id}", IP  = "{Ip}" , PORT = "{Port}" , USERNAME = "{UserName}" , PASSWORD = "{Password}" , NAME = "{Name}" , PANELURL = "{PanelUrl}" , STATUS = "{Status}" WHERE ID = "{Id}"'
            self.cursor.execute(query)
            self.conn.commit()
        else :
            return False

    def ChangeStep(self, UserId, NewValue) -> ChangeValue:
        return self.ChangeValue('USERS', 'step', NewValue, 'USERID', UserId)



def MakeVPN(XuiOBJ, Server, Days, GB):
    try:
        config = XuiOBJ.AddClient(Server, Days, GB)
        return config
    except Exception as e :
        print('Err')
        print(e)
        return False