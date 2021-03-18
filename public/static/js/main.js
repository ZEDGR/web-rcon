const app = Vue.createApp({
  data() {
    return {
      urlhost:
        location.protocol +
        "//" +
        location.hostname +
        (location.port ? ":" + location.port : ""),
      username: "",
      password: "",
      authenticated: Cookies.get("csrf_access_token") ? true : false,
      playerList: [],
      banList: [],
      selectedTab: "playerList",
    };
  },
  created() {
    axios.defaults.withCredentials = true;
    axios.defaults.xsrfCookieName = "csrf_access_token";
    axios.defaults.xsrfHeaderName = "X-CSRF-Token";
    axios.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        if (error.response.status === 401) {
          this.authenticated = false;
          alert("Invalid username/password or session expired");
        } else {
          alert("An error occurred please try again later");
        }
        return error;
      }
    );
    if (this.authenticated) {
      this.getPlayers();
      this.getBanList();
    }
  },
  watch: {
    authenticated() {
      if (this.authenticated) {
        this.getPlayers();
        this.getBanList();
      }
    },
  },
  methods: {
    login(e) {
      e.preventDefault();
      axios
        .post(`${this.urlhost}/login`, {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          this.authenticated = response.data.authenticated;
        });
    },
    logout() {
      axios.get(`${this.urlhost}/logout`);
      this.authenticated = "";
    },
    getPlayers() {
      axios.get(`${this.urlhost}/players`).then((response) => {
        this.playerList = response.data.players;
      });
    },
    kickPlayer(player) {
      const msg = `Kick player ${player.name} ?`;
      if (confirm(msg)) {
        axios
          .post(`${this.urlhost}/playerkick`, { num: player.num })
          .then((response) => {
            if (response.data.success) {
              alert(`Player ${player.name} has been kicked from the server`);
              this.getPlayers();
            } else {
              alert(`Player ${player.name} not found`);
            }
          });
      }
    },
    banPlayer(player) {
      const msg = `Ban player ${player.name} ?`;
      if (confirm(msg)) {
        axios
          .post(`${this.urlhost}/playerban`, {
            name: player.name,
            address: player.address,
            num: player.num,
          })
          .then((response) => {
            if (response.data.success) {
              alert(`Player ${player.name} has been banned from the server`);
              this.getPlayers();
            } else {
              alert(`Player ${player.name} not found`);
            }
          });
      }
    },
    getBanList() {
      axios.get(`${this.urlhost}/banlist`).then((response) => {
        this.banList = response.data.banList;
      });
    },
    removeBan(banRecord) {
      const msg = `Remove Ban for ${banRecord.name}`;
      if (confirm(msg)) {
        axios
          .post(`${this.urlhost}/removeban`, {
            ip: banRecord.ip,
          })
          .then((response) => {
            if (response.data.success) {
              alert(`Ban for ${banRecord.name} has been removed`);
              this.getBanList();
            } else {
              alert(`Ban not found for ${banRecord.name}`);
            }
          });
      }
    },
    changeTab(tabName) {
      this.selectedTab = tabName;
    },
  },
});

app.mount("#app");
