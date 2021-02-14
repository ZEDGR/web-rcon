import axios from "axios";

const BASE_URL = `http://localhost:3000/`;

export function kickPlayerAction(player, setPlayers) {
  axios
    .get(`${BASE_URL}playerkick/${player.num}`)
    .then((res) => {
      setPlayers(() => {
        return res.data;
      });
    })
    .catch((e) => {
      console.log(e);
    });
}

export function banPlayerAction(player) {}
