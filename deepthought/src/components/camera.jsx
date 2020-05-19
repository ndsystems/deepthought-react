import React, { Component } from "react";
import io from "socket.io-client";
import draw_image from "./mpl_image";

let socket = io("http://" + document.domain + ":5000", {
  transport: ["websocket"],
  "force new connection": true,
  resource: "socket/socket.io",
});

// change camera mode - 12bit/16bit

export default class Camera extends Component {
  constructor() {
    super();
    this.state = {
      exposure: 10,
      gain: 1,
    };

    this.styles = {
      fontSize: "15px",
      fontWeight: "bold ",
    };

    socket.on("image", (json_data) => {
      console.log(json_data);
      draw_image(json_data);
    });
  }

  getBadgeClasses() {
    let label_classes = "badge badge-primary m-2";
    let button_classes = "m-2 btn btn-secondary btn-sm";
    return { label_classes, button_classes };
  }

  eventHandler = (event) => {
    event.preventDefault();
    socket.emit("camera_props", this.state);

    // emit exposure change
  };

  setExposure = (e) => {
    this.setState({ exposure: e.target.value });
  };

  snap = () => {
    console.log("emitting");
    socket.emit("snap");
  };

  live() {
    socket.emit("live");
  }

  render() {
    let { label_classes, button_classes } = this.getBadgeClasses();

    return (
      <div>
        <h4>Camera Control</h4>

        <span style={this.styles} className={label_classes}>
          Exposure Time
          <form onSubmit={this.eventHandler}>
            <input
              id="exp_time"
              type="text"
              name=""
              placeholder={this.state.exposure}
              onChange={this.setExposure}
            />
            <input type="submit" hidden={true} />
          </form>
        </span>
        <br />

        <span style={this.styles} className={label_classes}>
          Gain
          <form onSubmit={this.setGain}>
            <input
              className="form-control-range"
              type="range"
              name="gain_slider"
              min="0"
              max="3"
              id=""
            />
          </form>
        </span>

        <br />

        <button className={button_classes} onClick={this.snap}>
          Snap
        </button>
        <button className={button_classes} onClick={this.live}>
          Live
        </button>
      </div>
    );
  }
}
