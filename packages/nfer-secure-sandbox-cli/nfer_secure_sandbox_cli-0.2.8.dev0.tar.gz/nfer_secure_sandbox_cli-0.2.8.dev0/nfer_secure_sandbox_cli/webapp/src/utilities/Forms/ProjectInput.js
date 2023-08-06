import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Form from 'react-bootstrap/Form';
import {Row, Col} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

class ProjectInput extends Component {
    constructor(props) {
        super(props);
        this.state = {name: "", desc: "", verbosity: "INFO"};
        //this.handleSubmit = this.handleSubmit.bind(this);
      }

//    handleSubmit(event) {
//        this.setState({name: document.getElementById('project_name').value});
//        this.setState({desc: document.getElementById('project_desc').value});
//        this.setState({verbosity: document.getElementById('project_verbosity').value});
//        console.log(this.state)
//    }

    render() {
	return (
	    <>
        <Form.Group>
            <Form.Label>Project Name</Form.Label>
            <Form.Control name="project_name" id="project_name" type="text" placeholder="Enter Project Name ..." />
            <Form.Text className="text-muted">
              A Name for your Project - you can identify this pipeline with (Algorithm+Dataset+Sandbox purpose)
            </Form.Text>
            <Form.Label style={{ marginTop: "5px" }}>Project Description</Form.Label>
            <Form.Control name="project_desc" id="project_desc" type="text" placeholder="Enter (Optional) Project Description ..." />
            <Form.Text className="text-muted">
              A Short Description for your Project. Optional.
            </Form.Text>
            <Form.Label style={{ marginTop: "5px" }}>Verbosity Level</Form.Label>
            <Form.Control name="project_verbosity" id="project_verbosity" as="select">
              <option>INFO</option>
              <option>WARN</option>
              <option>DEBUG</option>
            </Form.Control>
            <Form.Text className="text-muted">
              The inputs for various tasks as are sought, those shall be run and logged w.r.t set verbosity. More in the README/Documentation.
            </Form.Text>
            <Form.Label style={{ marginTop: "5px" }}>Pipeline Template ID</Form.Label>
            <Form.Control name="pipeline_template_id" id="pipeline_template_id" as="select">
              <option>f3595120-bfa4-48dc-a198-9cb642797007</option>
              <option disabled>d290f1ee-6c54-4b01-90e6-d701748f0811</option>
              <option disabled>d290f1ee-6c54-4b01-90e6-d701748f0821</option>
            </Form.Control>
            <Form.Text className="text-muted">
              The inputs for various tasks as are sought, those shall be run and logged w.r.t set verbosity. More in the README/Documentation.
            </Form.Text>
          </Form.Group>
	    </>
	);
    }
};

export default ProjectInput;

