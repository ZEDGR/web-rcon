const app = Vue.createApp({
  data() {
    return {
      urlhost:
        location.protocol +
        "//" +
        location.hostname +
        (location.port ? ":" + location.port : ""),
      rconPassword: "",
      authToken: localStorage.getItem("authToken") || "",
      playerList: [],
    };
  },
  created() {
    axios.defaults.xsrfHeaderName = "X-CSRFToken";
    axios.defaults.xsrfCookieName = "XSRF-TOKEN";
    if (this.authToken) {
      this.getPlayers();
    }
  },
  watch: {
    authToken() {
      if (this.authToken) {
        this.getPlayers();
      }
    },
  },
  methods: {
    login(e) {
      e.preventDefault();
      axios
        .post(`${this.urlhost}/login`, { rcon_password: this.rconPassword })
        .then((response) => {
          this.authToken = response.data.token;
          localStorage.setItem("authToken", this.authToken);
        })
        .catch((error) => {
          if (error.response.status == 401) {
            alert("Invalid Rcon Password");
          } else {
            console.log(error);
            alert("An error occurred please try again later");
          }
        });
    },
    logout() {
      localStorage.removeItem("authToken");
      this.authToken = "";
    },
    getPlayers() {
      axios
        .get(`${this.urlhost}/players`)
        .then((response) => {
          this.playerList = response.data.players;
        })
        .catch((error) => {
          console.log(error);
          alert("An error occurred please try again later");
        });
    },
    kickPlayer(player) {
      const msg = `Kick player ${player.name} ?`;
      if (confirm(msg)) {
        axios
          .post(`${this.urlhost}/playerkick`, { player_num: player.num })
          .then((response) => {
            if (response.data.success) {
              alert(`Player ${player.name} has been kicked from the server`);
            } else {
              alert(`Player ${player.name} not found`);
            }
          })
          .catch((error) => {
            console.log(error);
            alert("An error occurred please try again later");
          });
      }
    },
    banPlayer(player) {
      alert("This feature is not available yet");
    },
  },
});

app.mount("#app");
