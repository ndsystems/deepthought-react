import React, { Component } from "react";
import io from "socket.io-client";

let socket = io("http://localhost:5000");

class DeviceProperties extends Component {
  constructor() {
    super();
    this.state = { all_device_states: "" };

    socket.on("recv_device_states", (device_props) => {
      console.log(device_props);
      this.setState({ all_device_states: device_props });
    });
  }

  getDeviceProperties = () => {
    socket.emit("get_props");
  };

  render() {
    return (
      <div>
        <button
          className={"badge badge-primary m-2"}
          onClick={this.getDeviceProperties}
        >
          Update
        </button>

        <ul>
          {this.state.all_device_states.map((colleague, index) => {
            return <li key={index}>{colleague}</li>;
          })}
        </ul>
      </div>
    );
  }
}

export default DeviceProperties;
