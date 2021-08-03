import React, { Component } from "react";
import PropTypes from 'prop-types';


export default class RecordList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      records: [],
      loaded: false,
      placeholder: "Loading"
    };
    this.handleShowDetails = this.handleShowDetails.bind(this);
  }

  componentDidMount() {
    fetch(`api/records/?page_size=${20}`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState({records: data.results});
      });
  }

  handleShowDetails(recordId) {
    const {onShowDetails} = this.props;
    onShowDetails(recordId);
  }

  render() {
    const { records } = this.state;
    return (
      <div className="cat-bookList">
        <h1>Record List</h1>
        <table>
          <thead>
            <tr>
              <th>Id</th>
              <th>Title</th>
              <th>Author</th>
            </tr>
          </thead>
          <tbody>
          {records.map(record => {
            return (
              <tr key={record.id}>
                <td>{record.id}</td>
                <td onClick={() => this.handleShowDetails(record.id)}>{record.title}</td>
                <td>{record.author}</td>
              </tr>
            );
          })}
          </tbody>
        </table>
      </div>
    );
  }
}

RecordList.propTypes = {
  onShowDetails: PropTypes.func.isRequired
}
