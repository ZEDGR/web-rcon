import { useState, useEffect, useCallback } from "react";
import { Container } from "react-bootstrap";
import "./App.css";
import Header from "./components/Header";
import PlayerList from "./components/PlayerList";
import fetchPlayers from "./helpers/fetchPlayers";
import { kickPlayerAction, banPlayerAction } from "./helpers/playerActions";

function App() {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    fetchPlayers(setPlayers);
  }, []);

  return (
    <Container>
      <Header fetchPlayers={fetchPlayers} setPlayers={setPlayers} />
      <PlayerList
        players={players}
        setPlayers={setPlayers}
        kickPlayerAction={kickPlayerAction}
        banPlayerAction={banPlayerAction}
      />
    </Container>
  );
}

export default App;
