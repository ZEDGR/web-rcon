import React from "react";
import { Table } from "react-bootstrap";
import Player from "./Player";

function PlayerList({
  players,
  setPlayers,
  kickPlayerAction,
  banPlayerAction,
}) {
  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Score</th>
          <th>Address</th>
          <th>Ping</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {players.map((player) => {
          return (
            <Player
              key={player.num}
              player={player}
              setPlayers={setPlayers}
              kickPlayerAction={kickPlayerAction}
              banPlayerAction={banPlayerAction}
            />
          );
        })}
      </tbody>
    </Table>
  );
}

export default PlayerList;
