#Imports...
from .core import *

#Needs...
MoozDB = 'Mooz.db'
FirstChannel = 'MoozPanel'
SecondChannel = 'MoozPanel'

month = []



#Make DB
DB = database(MoozDB)
DB.MakeDB([
    "CREATE TABLE IF NOT EXISTS USERS(USERID VARCHAR(255), STEP VARCHAR(255), COIN VARCHAR(255) , ISADMIN TINYINT(1) DEFAULT 0 , ISBLOCKED TINYINT(1) DEFAULT 0);",
    "CREATE TABLE IF NOT EXISTS SETTINGS(NAME VARCHAR(255), VALUE VARCHAR(255));",
    "CREATE TABLE IF NOT EXISTS PLANS(ID VARCHAR(255), NAME VARCHAR(255), AMOUNT VARCHAR(255), PRICE VARCHAR(255), TIME VARCHAR(255));",
    "CREATE TABLE IF NOT EXISTS ORDERS(ID VARCHAR(255), USER VARCHAR(255), PLAN VARCHAR(255), STATUS VARCHAR(255));",
    "CREATE TABLE IF NOT EXISTS MONTHS(ID VARCHAR(255), NAME VARCHAR(255), DAYS VARCHAR(255));",
    "CREATE TABLE IF NOT EXISTS SERVERS(ID VARCHAR(255), IP VARCHAR(255), PORT VARCHAR(255), USERNAME VARCHAR(255), PASSWORD VARCHAR(255), NAME VARCHAR(255), PANELURL VARCHAR(255), STATUS VARCHAR(255), COOKIE VARCHAR(255), INBID VARCHAR(255));",
])

DB.WriteSettings('ch1' , FirstChannel )
DB.WriteSettings('ch2' , SecondChannel )
DB.WriteSettings('StartCoin' , 0)
DB.WriteSettings('AdminUserName' , 'Farzin_Acc')
DB.WriteSettings('welcome', 'سلام , به ربات موزپنل خوش اومدی.\nاز دکمه های زیر استفاده کن')
# DB.WriteSettings('start', 'از دکمه های زیر استفاده کن')
# DB.WriteSettings('problem', 'برای ربات مشکلی بوجود اومده , لطفا بعدا دوباره امتحان کن')
DB.WriteSettings('buyMOOZ', f'برای خرید به پیوی ادمین مراجعه کن :\n@{DB.GetSetting("AdminUserName")}')
DB.WriteSettings('buyVPN' , f'لطفا سرور مورد نظر را انتخاب کنید')
DB.WriteSettings('Months' , f'لطفا مدت دلخواه خود را انتخاب نمایید')
DB.WriteSettings('Plan', f'لطفا پلن مورد نظرتون رو انتخاب کنین')
DB.WriteSettings('BuyPlan', f'از چه طریقی مایل به خرید هستید؟')
DB.WriteSettings('CoinBuySuccess', f'خرید شما با موفقیت انجام شد')
DB.WriteSettings('CoinBuyFailed', f'موجودی شما کافی نمیباشد')
DB.WriteSettings('CardBuyProccess', f'لطفا رسید را بفرستید')
DB.WriteSettings('CardBuySended', f'به محض تایید شدن توسط ادمین کانفیگ شما ارسال خواهد شد')
# DB.WriteSettings('ref', f'برای دعوت دوستان خود از طریق لینک زیر اقدام کن :\nhttps://t.me/{BOT_USERNAME}?start=')
DB.WriteSettings('panel', 'سلام ادمین , به پنل مدیریت خوش اومدی.\nاز دکمه های زیر استفاده کن :')
DB.WriteSettings('SupportText' , f'در صورت وجود هرگونه مشکل لطفا با ادمین در تماس باشید :\n@{DB.GetSetting("AdminUserName")}')
DB.WriteSettings('Ticket' , 'لطفا مشکل خود را فقط در قالب یک پیام ارسال کنید')
DB.WriteSettings('TicketSuccess' , 'پیام شما ارسال شد.\nلطفا منتظر جواب از سمت پشتیبانی بمانید')
DB.WriteSettings('ChooseText', f'لطفا انتخاب کنید.')
DB.WriteSettings('MessagePanelText', f'لطفا نوع ارسال پیام را انتخاب کنید')
DB.WriteSettings('SendMessage', f'لطفا پیام خود را ارسال نمایید')
DB.WriteSettings('SendingMessage', f'در حال ارسال پیام...')
DB.WriteSettings('MessageSuccess', f'پیام شما ارسال شد...')
DB.WriteSettings('ChEditMsg', f'لطفا آیدی کانال را بدون @ بفرستید')
DB.WriteSettings('NotFree', f'این امکان فقط در نسخه اشتراکی امکان پذیر میباشد.\n@MoozPanel')