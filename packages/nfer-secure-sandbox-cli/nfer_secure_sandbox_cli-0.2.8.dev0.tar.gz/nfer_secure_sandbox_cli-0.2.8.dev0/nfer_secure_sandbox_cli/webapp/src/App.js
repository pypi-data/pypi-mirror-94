import { RBreadcrumb } from './utilities/Breadcrumbs';
import { ProjectInput, CertInput, AlgorithmInput, CodebaseInput, DataInput, SandboxInput } from './utilities/Forms';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Container from 'react-bootstrap/Container';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import React, { Component } from 'react';
import Tooltip from 'react-bootstrap/Tooltip';
import {Row, Col} from 'react-bootstrap';
import Modal from 'react-bootstrap/Modal';
import './App.css';

const renderTooltip = (props) => (
  <Tooltip id="button-tooltip" {...props}>
    Simple tooltip
  </Tooltip>
);

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {showModal: false};
    this.formAndDisplayYAML = this.formAndDisplayYAML.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleClose() {
    this.setState({showModal: false});
  };

  formAndDisplayYAML() {
    this.setState({showModal: true});
  }

  handleSubmit(event) {
    event.preventDefault();
    const data = {};
    for (let i=0; i < event.target.elements.length; i++) {
        const elem = event.target.elements[i];
        if (elem.hasOwnProperty('checked')) {
            if (elem['checked']) { data[elem.name] = elem.value }
        }
        else { data[elem.name] = elem.value }
    }
    console.log(data);
    fetch('http://localhost:5112/setup_project/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin':'*'
      },
      body: JSON.stringify(data)
    })
    this.setState({showModal: true});
  }

  render() {
  return (
    <>
        <Card className="text-center">
          <Card.Header>Project Essentials</Card.Header>
          <Card.Body>
            <Card.Title>Filling in details for Tasks defining the Project end-to-end</Card.Title>
            <Card.Text>
              Sections for the application(code+dependencies), certificates, pipeline identifiers etc. need to be defined below.
              <b> For more information</b>, visit the Documentation link given below.
            </Card.Text>
            <Button href="https://www.google.com/" variant="primary">Nfer-Sandbox-Cli Tutorials</Button>
          </Card.Body>
        </Card>
        <Form onSubmit={this.handleSubmit}>
        <Container style={{ marginTop: "10px" }} fluid>
            <Row>
                <Col>
                    <RBreadcrumb data={{'section':"Project"}}/>
                    <ProjectInput />
                </Col>
                <Col>
                    <RBreadcrumb data={{'section':"Codebase"}}/>
                    <CodebaseInput />
                </Col>
            </Row>
            <Row>
                <Col>
                    <RBreadcrumb data={{'section':"Certificates"}}/>
                    <CertInput />
                </Col>
                <Col>
                    <RBreadcrumb data={{'section':"Sandbox"}}/>
                    <SandboxInput />
                </Col>
            </Row>
            <Row>
                <Col>
                    <RBreadcrumb data={{'section':"Data I/O"}}/>
                    <DataInput />
                </Col>
                <Col>
                    <RBreadcrumb data={{'section':"Algorithm"}}/>
                    <AlgorithmInput />
                </Col>
            </Row>
            <Row className="justify-content-md-center">
            <Col></Col>
            <Col>
            <Button type="submit" style={{ marginTop: "10px", marginBottom: "10px" }} variant="success" block>Setup Project</Button>
            </Col>
            <Col></Col>
            </Row>
            <Row>
            <Modal centered size="lg" style={{width: "100%"}} show={this.state.showModal} onHide={this.handleClose}>
                <Modal.Header closeButton>
                  <Modal.Title>Project Config (as following `main.yml` file)</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                <iframe style={{width: "100%" }} id="frame" src="/main.yml" height="300px" frameBorder="0">
                </iframe>
                </Modal.Body>
              </Modal>
            </Row>
        </Container>
        </Form>
    </>
  );
  }
}

export default App;
