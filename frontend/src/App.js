import React, { useState, useEffect } from 'react';
import Container from "react-bootstrap/Container";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import FormControl from "react-bootstrap/FormControl";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Modal from "react-bootstrap/Modal";
import ProgressBar from "react-bootstrap/ProgressBar";
import Card from "react-bootstrap/Card";

import './App.css';



function QVideo() {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        Launch Modal
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Video Titel</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Video Beschreibung
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleClose}>
            Save
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

function QVideoCard({ vidTitle, vidDescr }){
  return (
    <Card style={{ width: '18rem' }}>
      <Card.Img variant="top" src="holder.js/100px180" />
      <Card.Body>
        <Card.Title>{vidTitle}</Card.Title>
        <Card.Text>{vidDescr}</Card.Text>
        <Button variant="primary">Abbrechen</Button>
      </Card.Body>
    </Card>
  );
}

function App({ videos }) {
  return (
    <Container>
      <h1>Remote Youtube Queue</h1>
      <p>Bitte einen Link einfügen</p>
      <Form.Control type="input" id="linkField"/>
      <Button variant="primary" id="downloadButton">Download</Button>
      <Row>
        {videos.map(video => <Col><QVideoCard vidTitle={video.title} vidDescr={video.description}/></Col>)}
      </Row>

    </Container>
  );
}

export default App;
