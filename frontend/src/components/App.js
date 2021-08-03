import React, { Component } from "react";
import { render } from "react-dom";
import RecordList from "./RecordList";
import RecordDetails from "./RecordDetails";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedRecordId: null
    }

    this.handleShowRecordDetails = this.handleShowRecordDetails.bind(this);
  }

  handleShowRecordDetails(id) {
    this.setState({selectedRecordId: id});
  }

  render() {
    const {selectedRecordId} = this.state;

    return (
      <div>
        {selectedRecordId ?
          <RecordDetails id={selectedRecordId} />
          :
          <RecordList onShowDetails={this.handleShowRecordDetails} />
        }
      </div>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);