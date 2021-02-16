import React from "react";
import { Button } from "react-bootstrap";

function Player({ player, setPlayers, kickPlayerAction }) {
  const kickPlayerHandler = () => {
    if (window.confirm(`Are you sure you want to kick player ${player.name}`)) {
      kickPlayerAction(player, setPlayers);
    }
  };
  return (
    <tr>
      <td>{player.num}</td>
      <td>{player.name}</td>
      <td>{player.score}</td>
      <td>{player.address}</td>
      <td>{player.ping}</td>
      <td>
        <Button variant="info" onClick={kickPlayerHandler}>
          Kick
        </Button>
        &nbsp;
        <Button variant="secondary">Ban</Button>
      </td>
    </tr>
  );
}

export default Player;
