function mpld3_load_lib(url, callback) {
  var s = document.createElement("script");
  s.src = url;
  s.async = true;
  s.onreadystatechange = s.onload = callback;
  s.onerror = function () {
    console.warn("failed to load library " + url);
  };
  document.getElementsByTagName("head")[0].appendChild(s);
}

function draw_image(json_data) {
  console.log("drawing");
  if (typeof mpld3 !== "undefined" && mpld3._mpld3IsLoaded) {
    // already loaded: just create the figure
    !(function (mpld3) {
      d3.select("#camera_feed").selectAll("*").remove();
      mpld3.draw_figure("camera_feed", json_data);
    })(mpld3);
  } else if (typeof define === "function" && define.amd) {
    // require.js is available: use it to load d3/mpld3
    require.config({ paths: { d3: "https://mpld3.github.io/js/d3.v3.min" } });
    require(["d3"], function (d3) {
      window.d3 = d3;
      mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.3.js", function () {
        d3.select("#camera_feed").selectAll("*").remove();
        mpld3.draw_figure("camera_feed", json_data);
      });
    });
  } else {
    // require.js not available: dynamically load d3 & mpld3
    mpld3_load_lib("https://mpld3.github.io/js/d3.v3.min.js", function () {
      mpld3_load_lib("https://mpld3.github.io/js/mpld3.v0.3.js", function () {
        d3.select("#camera_feed").selectAll("*").remove();
        mpld3.draw_figure("camera_feed", json_data);
      });
    });
  }
}
