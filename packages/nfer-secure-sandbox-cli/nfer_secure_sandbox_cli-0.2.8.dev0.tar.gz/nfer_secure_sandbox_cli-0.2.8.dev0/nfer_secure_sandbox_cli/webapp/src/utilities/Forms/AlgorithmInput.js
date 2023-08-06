import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Form from 'react-bootstrap/Form';
import {Row, Col} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

class AlgorithmInput extends Component {
    render() {
	return (
	    <>
        <Form.Group controlId="formBasicEmail">
            <Form.Label style={{ marginTop: "5px" }}>Algorithm Docker Image Details</Form.Label>
              <Form.Row>
                <Col>
                  <Form.Control name="image_name" placeholder="Image Name" />
                </Col>
                <Col>
                  <Form.Control name="image_repo"  placeholder="Image Repository" />
                </Col>
                <Col>
                  <Form.Control name="image_tag" placeholder="Image Tag" />
                </Col>
              </Form.Row>
            <Form.Text className="text-muted">
              Identifiers for the Docker Image of the Algorithm that shall be formed.
            </Form.Text>
          </Form.Group>
	    </>
	);
    }
};

export default AlgorithmInput;
