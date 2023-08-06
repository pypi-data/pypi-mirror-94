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

class DataInput extends Component {
    render() {
	return (
	    <>
	      <Form.Group as={Row}>
              <Form.Label column sm={3}>
                Projection ID for Input Dataset
              </Form.Label>
              <Col sm={9}>
                <OverlayTrigger placement="right" delay={{ show: 25, hide: 40 }} overlay={renderTooltip} popperConfig={{testObj:"genentech severe headache women data"}}>
                <Form.Check
                  type="radio"
                  label="genentech-headache-data"
                  name="input-dataprojection"
                  value="genentech-headache-data"
                  id="d290f1ee-6c54-4b01-90e6-d701748f0851"
                />
                </OverlayTrigger>
                <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }} overlay={renderTooltip} popperConfig={{testObj:"genentech's ankle sprain patient's data"}}>
                <Form.Check
                  type="radio"
                  label="genentech-sprain-data"
                  name="input-dataprojection"
                  value="genentech-sprain-data"
                  id="d290f1ee-6c54-4b01-90e6-d701748f0851"
                />
                </OverlayTrigger>
                <OverlayTrigger placement="right" delay={{ show: 250, hide: 400 }} overlay={renderTooltip} popperConfig={{testObj:"jansonn's rootcanal patients data"}}>
                <Form.Check
                  type="radio"
                  label="jansonn-rootcanal-data"
                  name="input-dataprojection"
                  value="jansonn-rootcanal-data"
                  id="d290f1ee-6c54-4b01-90e6-d701748f0851"
                />
                </OverlayTrigger>
                </Col>
                </Form.Group>
              <Form.Label style={{ marginTop: "5px" }}>Dataset Projection Name</Form.Label>
            <Form.Control name="projection_name" type="text" placeholder="Enter a name for the projection dataset ..." />
            <Form.Text className="text-muted">
              Optional. By default - the pipeline name accompanied by the data projection ID
            </Form.Text>
	    </>
	);
    }
};

export default DataInput;
