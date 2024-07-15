#Imports...
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import BadRequest , RPCError
from pyrogram import Client , filters
import logging , asyncio 
from MoozBot import *

#Database...
DB = config.DB

#Informations...
api_id = 000
api_hash = 'abc'
admin = 000
botUsername = ''
token = ''

#logging...
#logging.basicConfig( filename = 'mooz-excepts.txt' , filemode = 'a+'  )


#app
app = Client('MoozPanel' , api_id , api_hash , bot_token=token)



#Lets Code...
@app.on_message()
async def main(client , message) :
#    try :
    #-------------------------------------------------------
    adminList = DB.GetAdmins()
    adminList.append(admin)
    chat_id = message.chat.id
    userid = message.from_user.id
    ch1 = DB.GetSetting('ch1')
    ch2 = DB.GetSetting('ch2')
    tch1 = await app.get_chat_member(ch1, userid)
    tch2 = await app.get_chat_member(ch2, userid)
    #Check User Exists...
    if DB.GetUser(userid) == False :
        if userid in adminList :
            DB.MakeUser(userid,'start',int(DB.GetSetting('StartCoin')),True,False)
        else :
            DB.MakeUser(userid,'start',int(DB.GetSetting('StartCoin')),False,False)
    #Get UserInfo
    user = DB.GetUser(userid)
    userstep = str(user[1])
    #-------------------------------------------------------
    try :
        tt = message.entities
        if not tt == None :
            st = message.entities[0].type
            if st == 'bot_command' :
                id = message.text.partition(' ')
                if id[0] == '/start' and len(id) == 3 and not id[2] == '' :
                    if len(id[2]) > 12 :
                        #Here We Go Again...
                        app.send_message(userid , "Little Silly Hacker :)")
                    else :
                        #User Is Invited...
                        pass
    except BadRequest :
        await app.send_message(userid , "لطفا در کانال های اسپانسر عضو شوید 🙃" , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌱 چنل اول 🌱" , url = f'https://t.me/{ch1}') , InlineKeyboardButton("🎋 چنل دوم 🎋" , url = f'https://t.me/{ch2}')], [InlineKeyboardButton('✨ Confirm ✨' , url = 'https://t.me/{botUsername}')]]))
    #-------------------------------------------------------
    if message.text == '/panel' and userid in adminList : #Admin Panel...
        await app.send_message(userid , DB.GetSetting('panel'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🕊 آمار ربات 🕊" , callback_data = 'BotStats') , InlineKeyboardButton('✍🏻 پیام ها ✍🏻' , callback_data = 'MessagesPanel')], [InlineKeyboardButton('🎛 پنل ها 🎛' , callback_data = 'Panels')], [InlineKeyboardButton('📝 تیکت ها 📝' , callback_data = 'TicketsPanel'),InlineKeyboardButton("⚙️ تنظیمات ⚙️" , callback_data = 'Settings')]]))
    #-------------------------------------------------------
    if userstep == 'start' and message.text == '/start' :
        await app.send_message(userid , DB.GetSetting('welcome'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍌 خرید موز 🍌" , callback_data = 'BuyMooz') , InlineKeyboardButton("🍌 حساب کاربری 🍌" , callback_data = 'Account')], [InlineKeyboardButton('🍌 خرید کانفیگ 🍌' , callback_data = 'BuyVPN')], [InlineKeyboardButton('📝' , callback_data = 'Ticket'),InlineKeyboardButton('☎️' , callback_data = 'Support')]]))
    #-------------------------------------------------------
    elif userstep == 'Ticket' :
        await message.forward(DB.GetSetting("AdminUserName"),)
        await app.send_message(DB.GetSetting("AdminUserName"), f'Name: `{message.from_user.first_name}`\nLastName: `{message.from_user.last_name}`\nUserName: `{message.from_user.username}`\nUserId: `{userid}`')
        DB.ChangeStep(userid,'start')
        await message.reply(DB.GetSetting('TicketSuccess'))
        await app.send_message(userid , DB.GetSetting('welcome'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍌 خرید موز" , callback_data = 'BuyMooz') , InlineKeyboardButton("حساب کاربری 🍌" , callback_data = 'Account')], [InlineKeyboardButton('🍌 خرید کانفیگ 🍌' , callback_data = 'BuyVPN')], [InlineKeyboardButton('📝' , callback_data = 'Ticket'),InlineKeyboardButton('☎️' , callback_data = 'Support')]]))
    #-------------------------------------------------------
    elif userstep.startswith('CardBuy_') :
        DB.ChangeStep(userid,'start')
        oid , Server , Time = userstep.partition('CardBuy_')[2].split('/')[0],userstep.partition('CardBuy_')[2].split('/')[1],userstep.partition('CardBuy_')[2].split('/')[2]
        mkord = DB.WriteOrders(oid,userid,userid,'off')
        await message.forward(DB.GetSetting("AdminUserName"),)
        await app.send_message(DB.GetSetting("AdminUserName"),f'تایید میکنید؟', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("بله" , callback_data = f'Yes_{oid}/{Server}/{Time}')],[InlineKeyboardButton("خیر" , callback_data = f'No_{oid}')]]))
        await message.reply(DB.GetSetting('CardBuySended'))
        await app.send_message(userid , DB.GetSetting('welcome'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍌 خرید موز" , callback_data = 'BuyMooz') , InlineKeyboardButton("حساب کاربری 🍌" , callback_data = 'Account')], [InlineKeyboardButton('🍌 خرید کانفیگ 🍌' , callback_data = 'BuyVPN')], [InlineKeyboardButton('📝' , callback_data = 'Ticket'),InlineKeyboardButton('☎️' , callback_data = 'Support')]]))
    #-------------------------------------------------------
    #Admin Panel...
    elif userstep == 'SendAll' :
        DB.ChangeStep(userid,'start')
        users = DB.GetUsers
        await message.reply(DB.GetSetting('SendingMessage'))
        for i in users :
            await app.send_message(i[0],message.text)
        await app.send_message(userid,DB.GetSetting('MessageSuccess'),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif userstep == 'ForAll' :
        DB.ChangeStep(userid,'start')
        users = DB.GetUsers
        await message.reply(DB.GetSetting('SendingMessage'))
        for i in users :
            await message.forward(i[0])
        await app.send_message(userid,DB.GetSetting('MessageSuccess'),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif userstep in ['ch1edit','ch2edit'] :
        DB.ChangeStep(userid,'start')
        if userstep == 'ch1edit' :
            DB.WriteSettings('ch1' , message.text.replace('@',''))
            await message.reply(f"Ok Its Done.\nI Saved @{message.text.replace('@','')}")
        else :
            DB.WriteSettings('ch2' , message.text.replace('@',''))
            await message.reply(f"Ok Its Done.\nI Saved @{message.text.replace('@','')}")
    #-------------------------------------------------------
    elif userstep == 'ADDPLAN' :
        DB.ChangeStep(userid,'start')
        plan = message.text.split('\n')
        if not len(plan) == 4 :
            await message.reply('Please Send Correct Form...')
        else :
            DB.ChangeStep(userid,'start')
            plns = DB.GetPlans
            id = len(plns)
            DB.WritePlans(id,plan[0],plan[1],plan[2],plan[3])
            await message.reply(f'Ok I just saved the plan with this info :\n`Id : {id}\nName : {plan[0]}\nAmount : {plan[1]}\nPrice : {plan[2]}\nTime : {plan[3]}`')
    #-------------------------------------------------------
    elif userstep == 'AddServers' :
        DB.ChangeStep(userid,'start')
        server = message.text.split('\n')
        try :
            serverId = len(DB.GetServers)
            DB.WriteServers(serverId,server[0],server[1],server[2],server[3],server[4],server[5],True)
            await message.reply('Ok Its Done...')
        except :
            await message.reply('Aaah...\nPlease Try Again...')
    #-------------------------------------------------------
    elif userstep == 'AddMonth' :
        DB.ChangeStep(userid,'start')
        month = message.text.split('\n')
        monthId = len(DB.GetMonths)
        try :
            DB.WriteMonths(monthId,month[0],month[1])
            await message.reply('Ok Its Done...')
        except :
            await message.reply('Aaah...\nPlease Try Again...')
#    except BadRequest :
#        await app.send_message(userid , "لطفا در کانال های اسپانسر عضو شوید 🙃" , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌱 چنل اول 🌱" , url = f'https://t.me/{ch1}') , InlineKeyboardButton("🎋 چنل دوم 🎋" , url = f'https://t.me/{ch2}')], [InlineKeyboardButton('✨ Confirm ✨' , url = 'https://t.me/{botUsername}')]]))
#    except Exception as e :
#        print(e)


@app.on_callback_query()
async def callback(_, query) :
    adminList = DB.GetAdmins()
    adminList.append(admin)
    userid = query.from_user.id
    chat_id = query.message.chat.id
    message_id = query.message.id
    data = query.data
    #-------------------------------------------------------
    if data == 'BuyMooz' :
        DB.ChangeStep(userid,'BuyMooz')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('buyMOOZ') ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Back')]]))
    #-------------------------------------------------------
    if data == 'Account' :
        DB.ChangeStep(userid,'Account')
        us = DB.GetUser(userid)
        text = f'اطلاعات حساب کاربری 👤\n\n🆔 شناسه عددی: `{userid}`\n🍌 موجودی: {us[2]}\n\n@{DB.GetSetting("ch1")} - @{DB.GetSetting("ch2")}'
        await app.edit_message_text(chat_id , message_id , text ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Back')]]))
    #-------------------------------------------------------
    if data == 'BuyVPN' :
        DB.ChangeStep(userid,'BuyVPN')
        servers = DB.GetServers
        serverButtons = [InlineKeyboardButton(f'{i[5]}' , callback_data = f'Server_{i[0]}') for i in servers]
        serverButtons = [serverButtons[i:i+2] for i in range(0,len(serverButtons),2)]
        serverButtons.append([InlineKeyboardButton('🔙' , callback_data = 'Back')])
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('buyVPN') ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup(serverButtons))
    #-------------------------------------------------------
    if data == 'Ticket' :
        DB.ChangeStep(userid,'Ticket')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('Ticket') ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Back')]]))
    #-------------------------------------------------------
    if data == 'Support' :
        DB.ChangeStep(userid,'start')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('SupportText') ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Back')]]))
    #-------------------------------------------------------
    elif data == 'Back' :
        DB.ChangeStep(userid,'start')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('welcome') ) 
        await app.edit_message_reply_markup(chat_id , message_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🍌 خرید موز" , callback_data = 'BuyMooz') , InlineKeyboardButton("حساب کاربری 🍌" , callback_data = 'Account')], [InlineKeyboardButton('🍌 خرید کانفیگ 🍌' , callback_data = 'BuyVPN')], [InlineKeyboardButton('📝' , callback_data = 'Ticket'),InlineKeyboardButton('☎️' , callback_data = 'Support')]]))
    #-------------------------------------------------------
    elif data.startswith('Server_') :
        id = data.partition('Server_')[2]
        #Make Plan With ServerId
        months = DB.GetMonths
        buttons = [[InlineKeyboardButton(f'{i[1]}' , callback_data = f'Month_{i[0]}/{id}')] for i in months]
        buttons.append([InlineKeyboardButton('🔙' , callback_data = 'Back')])
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('Months') ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup(buttons))
    #-------------------------------------------------------
    elif data.startswith('Month_') :
        info = data.partition('Month_')[2].split('/')
        id = info[0]
        Server = info[1]
        Time = DB.GetMonth(id)[2]
        plans = DB.GetPlanM(Time)
        buttons = [[InlineKeyboardButton(f'{i[1]}' , callback_data = f'Plan_{i[0]}/{Server}/{Time[-1]}/{i[2]}')] for i in plans]
        buttons.append([InlineKeyboardButton('🔙' , callback_data = 'Back')])
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('Plan') ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup(buttons))
    #-------------------------------------------------------
    elif data.startswith('Plan_') :
        info = data.partition('Plan_')[2].split('/')
        id = info[0]
        Server = info[1]
        Days = info[2]
        Amount = info[3]
        buttons = [[InlineKeyboardButton('اعتبار حساب' , callback_data = f'CoinBuy_{id}/{Server}/{Days}/{Amount}'),InlineKeyboardButton('کارت به کارت' , callback_data = f'CardBuy_{id}/{Server}/{Days}')]]
        buttons.append([InlineKeyboardButton('🔙' , callback_data = 'Back')])
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('BuyPlan') ) 
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup(buttons))
    #-------------------------------------------------------
    elif data.startswith('CoinBuy_') :
        info = data.partition('CoinBuy_')[2].split('/')
        id = info[0]
        ServerID = info[1]
        Days = info[2]
        Amount = info[3]
        coins = DB.GetUser(userid)[2]
        plan = DB.GetPlan(id)
        if coins >= plan[3] :
            #Can Buy...
            ServerInfo = DB.GetServer(ServerID)
            inboundID = ServerInfo[-1]
            Cookie = ServerInfo[-2]
            Username = ServerInfo[3]
            Password = ServerInfo[4]
            Url = ServerInfo[6]
            ManageXui = xui(Url, Username, Password, Cookie)
            oid = len(DB.GetOrders)
            mkord = DB.WriteOrders(oid,userid,id,'on')
            vpn = MakeVPN(ManageXui, inboundID, Days, Amount)
            if vpn:
                await app.send_message(userid , f'Your Config : `{vpn}`')
                await app.edit_message_text(chat_id , message_id , DB.GetSetting('CoinBuySuccess') )
                await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Back')]]))
            else:
                # Can't create VPN cuz protocol or invalid username password
                ...
        else :
            #Coins Are Not Enough...
            await app.edit_message_text(chat_id , message_id , DB.GetSetting('CoinBuyFailed') )
            await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Back')]]))
    #-------------------------------------------------------
    elif data.startswith('CardBuy_') :
        id = data.partition('CardBuy_')[2]
        DB.ChangeStep(userid,data)
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('CardBuyProccess') )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Back')]]))
    #-------------------------------------------------------
    #Admin Panel...
    elif data == 'BotStats' :
        DB.ChangeStep(userid,'start')
        stats = f'Stats : {len(DB.GetUsers)}\nOrders : {len(DB.GetOrders)}\nAdmins : {len(DB.GetAdmins())}\nServers : {len(DB.GetServers)}\nPlans : {len(DB.GetPlans)}'
        await app.edit_message_text(chat_id , message_id , stats )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))    
    #-------------------------------------------------------
    elif data == 'MessagesPanel' :
        DB.ChangeStep(userid,'start')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('MessagePanelText') )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('ارسال همگانی' , callback_data = 'SendAll'),InlineKeyboardButton('فوروارد همگانی' , callback_data = 'ForAll')],[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
     #-------------------------------------------------------
    elif data == 'SendAll' :
        DB.ChangeStep(userid,'SendAll')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('SendMessage') )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
     #-------------------------------------------------------
    elif data == 'ForAll' :
        DB.ChangeStep(userid,'ForAll')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('SendMessage') )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data == 'Settings' :
        DB.ChangeStep(userid,'start')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('ChooseText') )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton("🪙 سکه ها 🪙" , callback_data = 'CoinsPanel') , InlineKeyboardButton("🦢 ادمین ها 🦢" , callback_data = 'AdminsPanel')], [InlineKeyboardButton('🔒 کانال ها 🔒' , callback_data = 'ChannelsPanel')], [InlineKeyboardButton('✏️ متن دکمه ها ✏️' , callback_data = 'ButtonTexts'),InlineKeyboardButton('✏️ متن پنل ها ✏️' , callback_data = 'PanelTexts')],[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))   
    #-------------------------------------------------------
    elif data == 'CoinsPanel' or data == 'ButtonTexts' or data == 'PanelTexts' or data == 'TicketsPanel' :
        DB.ChangeStep(userid,'start')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('NotFree') )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data == 'AdminsPanel' :
        DB.ChangeStep(userid,'start')
        admins = adminList.remove(admin)
        text = f'Moderator : `{admin}`\nAdmins List : \n'
        if admins == None :
            text += '`Nobody :)`'
        else :
            for i in admins :
                text += f'`{i}`\n'
        await app.edit_message_text(chat_id , message_id , text )
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data == 'ChannelsPanel' :
        DB.ChangeStep(userid,'start')
        text = f"First Channel : @{DB.GetSetting('ch1')}\nSecond Channel : @{DB.GetSetting('ch2')}"
        await app.edit_message_text(chat_id , message_id , text)
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('Edit First Channel' , callback_data = 'ch1edit'),InlineKeyboardButton('Edit Second Channel' , callback_data = 'ch2edit')],[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data in ['ch1edit','ch2edit'] :
        DB.ChangeStep(userid,data)
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('ChEditMsg'))
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data == 'Panels' :
        DB.ChangeStep(userid,'start')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('ChooseText'))
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('Edit Plans' , callback_data = 'EditPlans'),InlineKeyboardButton('Edit Month' , callback_data = 'EditMonth')],[InlineKeyboardButton('Edit Servers' , callback_data = 'EditServers')],[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data == 'EditPlans' :
        DB.ChangeStep(userid,'start')
        plans = DB.GetPlans
        buttons = [[InlineKeyboardButton(f'{i[1]}' , callback_data = f'PLAN-{i[0]}')] for i in plans] + [[InlineKeyboardButton('Add Plan' , callback_data = 'ADDPLAN'),InlineKeyboardButton('🔙' , callback_data = 'Backp')]]
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('ChooseText'))
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup(buttons))
    #-------------------------------------------------------
    elif data == 'ADDPLAN' :
        DB.ChangeStep(userid,'ADDPLAN')
        await app.edit_message_text(chat_id , message_id , f'Please Send Plan Info In This Form :\n`Name - Just A Name For This Plan\nAmount - Amount In GB\nPrice - Price In Toman\nTime - Time In Days`')
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data == 'EditMonth' :
        DB.ChangeStep(userid,'start')
        month = DB.GetMonths
        buttons = [[InlineKeyboardButton(f'{i[1]}',callback_data=f'MONTH-{i[0]}')] for i in month] + [[InlineKeyboardButton('Add Month',callback_data='AddMonth'),InlineKeyboardButton('🔙' , callback_data = 'Backp')]]
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('ChooseText'))
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup(buttons))
    #-------------------------------------------------------
    elif data == 'AddMonth' :
        DB.ChangeStep(userid,'AddMonth')
        await app.edit_message_text(chat_id , message_id , f'Please Send Month In This Form :\n`Name - Just A Name For It\nDays - Number Of Days`')
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data == 'EditServers' :
        DB.ChangeStep(userid,'start')
        servers = DB.GetServers
        buttons = [[InlineKeyboardButton(f'{i[5]}' , callback_data= f'SERVER-{i[0]}') for i in servers]]+[[InlineKeyboardButton('Add Server' , callback_data='AddServers')],[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('ChooseText'))
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup(buttons))
    #-------------------------------------------------------
    elif data == 'AddServers' :
        DB.ChangeStep(userid,'AddServers')
        await app.edit_message_text(chat_id , message_id , f'Please Send Plan Info In This Form :\n`Ip - Ip Or Domain Of Panel\nPort - Port Of Panel\nUsername - Username Of Panel\nPassword - Password Of Panel\nName - Name Of Panel\nPanelUrl - Complete URL Of Panel\nInboundID - Inbound Id For Making Configs`')
        await app.edit_message_reply_markup(chat_id , message_id , InlineKeyboardMarkup([[InlineKeyboardButton('🔙' , callback_data = 'Backp')]]))
    #-------------------------------------------------------
    elif data.startswith('Yes_') :
        info = data.partition('Yes_')[2].split('/')
        oid , Server , Time = info[0],info[1],info[2]
        Order = DB.GetOrder(oid)
        Amount = Order[2]
        ServerInfo = DB.GetServer(Server)
        inboundID = ServerInfo[-1]
        Cookie = ServerInfo[-2]
        Url = ServerInfo[6]
        Username = ServerInfo[3]
        Password = ServerInfo[4]
        #try :
        ManageXui = xui(Url, Username, Password, Cookie)
        vpn = MakeVPN(ManageXui, inboundID, Time, Amount)
        if vpn:
            await app.send_message(Order[1] , f'کانفیگ شما آماده است :`{vpn}`')
        else:
            await app.send_message(DB.GetSetting('AdminUserName') , f'Something Wrong With Making Config...\n{ServerInfo}\n{DB.GetOrder(oid)}')
        #except InvalidUsernameOrPassword :
        #    await  app.send_message(DB.GetSetting('AdminUserName'),f'Username Or Password Is Wrong...\n{str(ServerInfo)}')
        #except :
        #    await  app.send_message(DB.GetSetting('AdminUserName'),f'Something Wrong With This Server :\n{str(ServerInfo)}')

        #Make VPN Here...
    #-------------------------------------------------------
    elif data.startswith('No_') :
        pass
    #-------------------------------------------------------
    elif data == 'Backp' :
        DB.ChangeStep(userid,'start')
        await app.edit_message_text(chat_id , message_id , DB.GetSetting('welcome') ) 
        await app.edit_message_reply_markup(chat_id , message_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🕊 آمار ربات 🕊" , callback_data = 'BotStats') , InlineKeyboardButton('✍🏻 پیام ها ✍🏻' , callback_data = 'MessagesPanel')], [InlineKeyboardButton('🎛 پنل ها 🎛' , callback_data = 'Panels')], [InlineKeyboardButton('📝 تیکت ها 📝' , callback_data = 'TicketsPanel'),InlineKeyboardButton("⚙️ تنظیمات ⚙️" , callback_data = 'Settings')]]))
    #-------------------------------------------------------



#Run...
app.run()



