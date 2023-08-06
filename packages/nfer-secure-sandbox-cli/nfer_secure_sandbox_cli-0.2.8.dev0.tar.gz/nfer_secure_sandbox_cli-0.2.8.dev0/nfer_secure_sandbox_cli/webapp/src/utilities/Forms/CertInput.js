import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Form from 'react-bootstrap/Form';
import {Row, Col} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

class CertInput extends Component {
    render() {
	return (
	    <>
	      <Form.Group as={Row}>
              <Form.Label column sm={2}>
                Mode of Certificates
              </Form.Label>
              <Col sm={10}>
                <Form.Check
                  type="radio"
                  label="From CA"
                  name="source"
                  id="formHorizontalRadios1"
                  value="CA"
                />
                <Form.Check
                  type="radio"
                  label="Self Signed"
                  name="source"
                  id="formHorizontalRadios1"
                  value="self-signed"
                />
              </Col>
            </Form.Group>
          <Form.Group as={Row}>
              <Form.Label column sm={2}>
                Retrieval of Certs
              </Form.Label>
              <Col sm={10}>
                <Form.Check
                  type="radio"
                  label="Fetch Existing"
                  name="mode"
                  id="formHorizontalRadios2"
                  value="fetch"
                />
                <Form.Check
                  type="radio"
                  label="Create New Self-Signed"
                  name="mode"
                  value="create"
                  id="formHorizontalRadios2"
                />
              </Col>
            </Form.Group>
            <Form.File id="exampleFormControlFile1" label="Upload CA Certificates" />
	    </>
	);
    }
};

export default CertInput;
