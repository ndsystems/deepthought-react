import React, { Component } from "react";

const Toggle = ({ name, labelNameA, labelNameB }) => {
  return (
    <span style={this.styles} className="badge badge-primary m-2">
      EPI
      <input type="radio" value="open" name={name} /> {labelNameA}
      <input type="radio" value="close" name={name} defaultChecked />{" "}
      {labelNameB}
    </span>
  );
};

class Shutter extends Component {
  constructor(props) {
    super(props);
    this.state = { epi: "close", dia: "close", auto: "on" };
    this.styles = {
      fontSize: "15px",
      fontWeight: "bold ",
    };
  }

  setShutter = (e) => {
    this.setState({ [e.target.name]: e.target.value });
    console.log(this.state);
  };

  render() {
    return (
      <div onChange={this.setShutter}>
        <h4>Shutter Control</h4>
        <span style={this.styles} className="badge badge-primary m-2">
          EPI
          <input type="radio" value="open" name="epi" /> Open
          <input type="radio" value="close" name="epi" defaultChecked /> Close
        </span>
        <span style={this.styles} className="badge badge-primary m-2">
          DIA
          <input type="radio" value="open" name="dia" /> Open
          <input type="radio" value="close" name="dia" defaultChecked /> Close
        </span>

        <span style={this.styles} className="badge badge-primary m-2">
          Autoshutter
          <input type="radio" value="on" name="auto" defaultChecked /> On
          <input type="radio" value="off" name="auto" /> Off
        </span>
      </div>
    );
  }
}

export default Shutter;
