import eel
from flask import Flask, request
import webbrowser
import threading
import requests
import os
import json

app = Flask(__name__)

CLIENT_ID = 1172646785030832230
CLIENT_SECRET = 'WlGoqO8YULJz3iw-qq0hsOQhfS5DKQLC'

discordData = {
    'username': None,
    'discriminator': None,
    'id': None,
    'avatar': None
}

@eel.expose
def connectServer(ip):
    os.system(f'explorer.exe fivem://{ip}')

@eel.expose
def getResponse(url, url2):
    maxPlayers = 'Unknown'
    online = False
    response = requests.get(url)
    
    if response.status_code == 200:
        online = True
        js = response.json()
        maxPlayers = js['vars']['sv_maxClients']
    
    response = requests.get(url2)
    players = 'Unknown'
    if response.status_code == 200:
        players = len(response.json())
    
    result = {
        'online': online,
        'players': players,
        'maxPlayers': maxPlayers
    }
    
    return result

@eel.expose
def logout():
    path = os.path.join(os.getcwd(), 'user-config.json')
    if os.path.isfile(path):
        os.remove(path)
        
    exit(1)

@eel.expose
def readAuth():
    path = os.path.join(os.getcwd(), 'user-config.json')
    if os.path.isfile(path):
        reader = open(path, 'r')
        data = reader.read()
        reader.close()
        return json.loads(data)
        
    return False

@eel.expose
def setAuth(data):
    path = os.path.join(os.getcwd(), 'user-config.json')
    writer = open(path, 'w')
    writer.write(data)
    writer.close()

@eel.expose
def connectDiscord():
    webbrowser.open('https://discord.com/api/oauth2/authorize?client_id=1172646785030832230&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A27400%2Foauth2&scope=identify')

@app.route('/oauth2')
def oauth2():
    global discordData
    
    code = request.args.get('code')
    url = 'https://discord.com/api/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:27400/oauth2',
        'scope': 'identify guilds.join'
    }
    
    response = requests.post(url, headers=headers, data=data).json()
    accessToken = response['access_token']

    url = 'https://discord.com/api/users/@me'
    headers = {
        'Authorization': f'Bearer {accessToken}'
    }
    response = requests.get(url, headers=headers).json()
    
    username = response['username']
    discriminator = response['discriminator']
    userId = response['id']
    avatar = response['avatar']
    
    discordData['username'] = username
    discordData['discriminator'] = discriminator
    discordData['id'] = userId
    discordData['avatar'] = avatar
    
    eel.setDiscordData(discordData)
    
    return f'เชื่อมบัญชี Discord สำเร็จ เข้าสู่ระบบในชื่อ {username}! คุณสามารถปิดหน้าต่างนี้ไปได้เลย'

def closeCallback(route, webSockets):
    if not webSockets:
        os.system('taskkill /IM FiveM.exe /IM FiveM.exe /F')
        exit(1)

def startHost():
    app.run('0.0.0.0', 27400)

if __name__ == '__main__':
    x = threading.Thread(target=startHost, args=())
    x.start()
    
    eel.init('web', allowed_extensions=['.js', '.html'])
    eel.start(
        'main.html',
        mode='chrome',
        host='localhost',
        port=27500,
        block=True,
        size=(950, 600),
        position=(0, 0),
        disable_cache=False,
        close_callback=closeCallback,
        cmdline_args=['--incognito', '--no-experiments']
    )