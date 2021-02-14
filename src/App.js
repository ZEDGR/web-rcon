import { useState, useEffect, useCallback } from "react";
import { Container, Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRedoAlt } from "@fortawesome/free-solid-svg-icons";
import "./App.css";
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
      <h1 className="text-center">Web Rcon</h1>
      <Button
        className="float-right"
        variant="light"
        onClick={() => {
          fetchPlayers(setPlayers);
        }}
      >
        <FontAwesomeIcon icon={faRedoAlt} />
      </Button>
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
