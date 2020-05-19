import React from "react";
import ReactDOM from "react-dom";
import "bootstrap/dist/css/bootstrap.css";
// import Stage from "./components/stage";
import Camera from "./components/camera";
import Shutter from "./components/shutter";

// ReactDOM.render(<Stage />, document.getElementById("stage"));
ReactDOM.render(<Camera />, document.getElementById("camera_control"));
ReactDOM.render(<Shutter />, document.getElementById("shutter_control"));
