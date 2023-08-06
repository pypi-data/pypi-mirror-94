import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Form from 'react-bootstrap/Form';
import {Row, Col} from 'react-bootstrap';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import 'bootstrap/dist/css/bootstrap.min.css';

function renderTooltip(props) {
  let message = ""
  if (props.popper.state) {
        message = props.popper.state.options.testObj
    }
  return (
        <Tooltip id="button-tooltip" {...props}>
            {message}
        </Tooltip>
    );
}

class SandboxInput extends Component {
    render() {
	return (
	    <>
	      <Form.Group as={Row}>
              <Form.Label column sm={3}>
                Template for Sandbox VM
              </Form.Label>
              <Col sm={9}>
                <OverlayTrigger placement="left" delay={{ show: 25, hide: 40 }} overlay={renderTooltip} popperConfig={{testObj:"standard_sandbox_platform"}}>
                <Form.Check
                  type="radio"
                  label="standard_sandbox_platform"
                  name="sandboxVM"
                  value="55e5f812-488d-476d-8e9d-1cf58d369350"
                  id="55e5f812-488d-476d-8e9d-1cf58d369350"
                />
                </OverlayTrigger>
                <OverlayTrigger placement="left" delay={{ show: 250, hide: 400 }} overlay={renderTooltip} popperConfig={{testObj:"earlier_sandbox_platform"}}>
                <Form.Check
                  type="radio"
                  label="earlier_sandbox_platform"
                  name="sandboxVM"
                  value="d290f1ee-6c54-4b01-90e6-d701748f0851"
                  id="d290f1ee-6c54-4b01-90e6-d701748f0851"
                />
                </OverlayTrigger>
              </Col>
          </Form.Group>
	    </>
	);
    }
};

export default SandboxInput;
