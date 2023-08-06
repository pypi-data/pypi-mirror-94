import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { Breadcrumb } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

class RBreadcrumb extends Component {
    render() {
	return (
	    <>
        <Breadcrumb>
          <Breadcrumb.Item href="#">Configuration</Breadcrumb.Item>
          <Breadcrumb.Item href="#">
            Details
          </Breadcrumb.Item>
          <Breadcrumb.Item active>{this.props.data.section}</Breadcrumb.Item>
        </Breadcrumb>
	    </>
	);
    }
};

export default RBreadcrumb;
