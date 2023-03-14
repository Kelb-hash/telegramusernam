"""
 import the sync module from Telethon library.
"""
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from time import sleep
import sys
import csv
import traceback
import time
import random


"""
instantiate your client object using the credentials you got before.
"""

api_id =
api_hash = ''
phone = ''
client = TelegramClient(phone, api_id, api_hash)


"""
 connecting to telegram and checking if you are already authorized. Otherwise send
 an OTP code request and ask user to enter the code they received on their telegram account.
"""

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter Code Here: '))

users = []
with open('members.csv', encoding='UTF-8') as f:
    row = csv.reader(f, delimiter=",", lineterminator="\n")
    next(row, None)
    for row in row:
        user = {}
        user['username'] = row[0]
        users.append(user)

"""
offset_date and  offset_peer are used for filtering the chats.
We are sending empty values to these parameters so API returns all chats.
 offset_id and limit are used for pagination. Here we are getting last 300 chats of the user."""

chats = []
last_date = None
chuck_size = 300
groups = []


result = client(GetDialogsRequest(
    offset_date=last_date,  # offset_date and  offset_peer are used for filtering the chats
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chuck_size,
    hash=0
))

"""
Listing All Telegram Groups
"""

chats.extend(result.chats)


for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

""""
Ask User to Select a Group to Scrape Members

After listing the groups, prompt the user to input a number and select the
 group they want. When this code is executed it loops through every group that you
 stored in previous step and print it’s name starting with a number.
  This number is the index of that is your group list.
"""
print('Choose a group to add members from: ')
icon = 0

for g in groups:

    print(str(icon) + "- " + g.title)

    icon += 1

"""
Ask user to enter a number associated with a group.
 Then use this number as index to get the target group.
"""

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

"""
Get the group entity.
"""
target_group_entity = InputPeerChannel(
    target_group.id, target_group.access_hash)

"""
For adding the user we need to get the user entity first. There is two options to do this.

First let’s ask the user which mode they want and then we will explain them one by one.

"""

mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

# user_to_add = client.get_input_entity(user['username'])
# user_to_add = InputPeerUser(user['id'], user['access_hash'])


"""
Add Members to the Selected Group
Now you have the users in  users  list and the selected group in  target_group .
 We will use  InviteToChannelRequest function to the add 
 a user to the group. So let’s import it first.

"""

"""
Then you need to get the user based on the entered mode (i.e by ID or by user name.
"""

n = 0

for alluser in users:
    n += 1
    if n % 50 == 0:
        sleep(10)
    try:

        if mode == 1:
            if alluser['username'] == "":
                continue
            user_to_add = client.get_input_entity(alluser['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting for 5-10 Seconds...")
        time.sleep(random.randrange(5, 10))
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
 if user['username'] === '@skylineict':
  exception usernotfound:
   print("username not allowed to add in the group")
