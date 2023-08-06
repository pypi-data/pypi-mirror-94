import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Form from 'react-bootstrap/Form';
import {Row, Col} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

class CodebaseInput extends Component {
    render() {
	return (
	    <>
        <Form.Group controlId="formBasicEmail">
            <Form.Label>Git Repo URL</Form.Label>
            <Form.Control type="text" name="git_url" placeholder="Enter Git URL e.g https://github.com/<user>/<repo> ..." />
            <Form.Text className="text-muted">
              Github Repository URL. This repo contains the code and dependencies specifications.
            </Form.Text>
            <Form.Label style={{ marginTop: "5px" }}>Github Credentials</Form.Label>
              <Form.Row>
                <Col>
                  <Form.Control name="creds_user" placeholder="Username" />
                </Col>
                <Col>
                  <Form.Control name="creds_pass" type="password" placeholder="Password" />
                </Col>
              </Form.Row>
            <Form.Text className="text-muted">
              For 2FA Enabled, enter the API TOKEN, else, enter the Password
            </Form.Text>
            <Form.Label style={{ marginTop: "5px" }}>Stack</Form.Label>
            <Form.Control name="stack" id="stack" as="select">
              <option name="stack" value="Python3">Python3</option>
              <option name="stack" value="GO" disabled>GO</option>
              <option name="stack" value="R" disabled>R</option>
            </Form.Control>
            <Form.Text className="text-muted">
              The template, language of the developer's code. Python3 by default. Only Python3 supported. More on README.
            </Form.Text>
            <Form.Label style={{ marginTop: "5px" }}>Main Code File</Form.Label>
            <Form.Control name="code_file" type="text" placeholder="Enter the relative location of the main Algorithm file ..." />
            <Form.Text className="text-muted">
              e.g for entry point in src/ folder, specify : src/algo.py, should algo.py be the name of the entry/driver file
            </Form.Text>
            <Form.Label style={{ marginTop: "5px" }}>Dependency File</Form.Label>
            <Form.Control name="deps_file" type="text" placeholder="Enter the relative location of the requirements(.txt) file ..." />
            <Form.Text className="text-muted">
              e.g for deps file in deps/ folder, specify : deps/requirements.txt. Prefer filename requirements.txt for Python3 stack.
            </Form.Text>
          </Form.Group>
	    </>
	);
    }
};

export default CodebaseInput;
