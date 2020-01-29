"use strict"

var canvas = document.getElementById('shapes');
var ctx = canvas.getContext('2d');
var corners = [
  {x:10, y:10}, 
  {x:60, y:10}, 
  {x:60, y:80}, 
  {x:10, y:80}
  ];

//drawLabeledDot({x:250, y:100}, 20, "red", "1", "white");
//drawDot({x:100, y:50}, 10, "green");
//drawLine(corners[0], corners[1], 3, "white");

function clearCanvas() {
}


function callDrawPolygon() {
  drawPolygon(corners, 5, "red");
}

function drawPolygon(points, line_width, color) {
  ctx.beginPath();
  ctx.lineWidth = line_width;
  ctx.strokeStyle = color;
  ctx.moveTo(points[0].x, points[0].y);
  for (var i=1; i<points.length; i++) {
    ctx.lineTo(points[i].x, points[i].y);
  }
  ctx.lineTo(points[0].x, points[0].y);
  ctx.stroke();
  //ctx.fill();
}


function drawDot(center, radius, color) {
  ctx.beginPath();
  ctx.arc(center.x, center.y, radius, 0 , 2 * Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
}

function drawLabeledDot(center, radius, color, label, textColor) {
  ctx.beginPath();
  ctx.arc(center.x, center.y, radius, 0 , 2 * Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.font = "bold " + radius + "px Courier New";
  ctx.textBaseline = "middle";
  ctx.textAlign = "center";
  ctx.fillStyle = textColor;
  ctx.fillText(label, center.x, center.y);
}

function drawLine(pt_start, pt_end, line_width, color) {
  ctx.beginPath();
  ctx.lineWidth = line_width;
  ctx.strokeStyle = color;
  ctx.moveTo(pt_start.x, pt_start.y);
  ctx.lineTo(pt_end.x, pt_end.y);
  ctx.stroke();
  //ctx.closePath();
}
