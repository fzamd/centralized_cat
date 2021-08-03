import React, { Component } from "react";
import PropTypes from 'prop-types';


export default class RecordDetails extends Component {
  constructor(props) {
    super(props);
    this.state = {
      record: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

 componentDidMount() {
   const {id} = this.props;

   fetch(`api/records/${id}`, {
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
       this.setState({record: data});
     });
 }

  render() {
    const {record} = this.state;

    return (
      <div className="cat-bookDetails">
        <h1>Book Details for #{record.id}</h1>
        <div className="cat-bookDetails-header">
          <h2>{record.title}</h2>
          <div className="cat-bookDetails-info">
            <img src="https://w7.pngwing.com/pngs/808/1018/png-transparent-e-book-computer-icons-reading-book-icon-angle-reading-logo-thumbnail.png" width="220" height="240"/>
            <p>{record.subtitle}</p>
          </div>
        </div>
        <div className="cat-bookDetails-biblio">
          <h2>Bibliographic information</h2>
          <table>
            <tr>
              <td>Title</td>
              <td>{record.title}</td>
            </tr>
            <tr>
              <td>Author</td>
              <td>{record.author}</td>
            </tr>
            <tr>
              <td>Publisher</td>
              <td>{record.publisher}</td>
            </tr>
            <tr>
              <td>Publisher</td>
              <td>{record.publisher}, {record.publish_year}</td>
            </tr>
            <tr>
              <td>Source</td>
              <td>{record.publisher}, {record.publish_year}</td>
            </tr>
          </table>
        </div>
      </div>
    );
  }
}

RecordDetails.propTypes = {
  id: PropTypes.number.isRequired,
}