import axios from "axios";

const BASE_URL = `http://localhost:3000/`;

export default function fetchPlayers(setPlayers) {
  fetch(`${BASE_URL}players`)
    .then((res) => res.json())
    .then((data) => setPlayers(data));
}
