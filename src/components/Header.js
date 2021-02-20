import React from "react";
import { Button, Container, Row } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRedoAlt } from "@fortawesome/free-solid-svg-icons";

function Header({ fetchPlayers, setPlayers }) {
  return (
    <header>
      <Container>
        <Row className="justify-content-center">
          <h1>Web Rcon</h1>
        </Row>
        <Row className="float-right">
          <Button
            variant="light"
            onClick={() => {
              fetchPlayers(setPlayers);
            }}
          >
            <FontAwesomeIcon icon={faRedoAlt} />
          </Button>
        </Row>
      </Container>
    </header>
  );
}

export default Header;
