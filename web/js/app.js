const init = () => ({
    serverActive: 0,
    serverLists: [
        ['2K Community Server 1', '43.229.148.226'],
        ['2K Community Server 2', '43.229.148.226']
    ],
    page: 'connection',
    discord: false,
    discordConnecting: false,
    overlay: false,
    disable: false,
    serverData: {
        online: true,
        players: 0,
        maxPlayers: 600,
    },
    connectServer() {
        let targetServer = this.serverLists[this.serverActive];
        let ip = targetServer[1];

        this.disable = true;
        eel.connectServer(ip);
        setTimeout(() => {
            this.disable = false;
        }, 5000);
    },
    logout() {
        eel.logout();

        setTimeout(() => {
            window.open('', '_self').close();
        }, 100);
    },
    connectDiscord() {
        this.discordConnecting = true;
        eel.connectDiscord();
    },
    async setActiveServer(id) {
        this.serverActive = id;

        let targetServer = this.serverLists[this.serverActive];
        let ip = targetServer[1];
        let fullEndpointInfo = `http://${ip}:30120/info.json`;
        let fullEndpointPlayers = `http://${ip}:30120/players.json`;

        let response = await eel.getResponse(fullEndpointInfo, fullEndpointPlayers)();
        
        this.serverData.online = response.online;
        this.serverData.players = response.players;
        this.serverData.maxPlayers = response.maxPlayers;
    },
    async listener() {
        this.discord = await eel.readAuth()();

        if(this.discord !== false) {
            try {
                let newDiscord = this.discord;
                this.discord = newDiscord;

                this.page = 'home';
                this.overlay = true;
            } catch(e) {}
        }

        this.setActiveServer(0);
        
        const setParentData = (data) => {
            this.discord = data;
            this.discordConnecting = false;
            this.page = 'home';
            this.overlay = true;
        }

        eel.expose(setDiscordData);
        function setDiscordData(data) {
            eel.setAuth(JSON.stringify(data));
            setParentData(data);
        }
    }
});