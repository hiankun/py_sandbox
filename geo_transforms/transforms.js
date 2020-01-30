"use strict"

var canvas = document.getElementById('shapes');
var ctx = canvas.getContext('2d');

var corners = [
  {x:10, y:10}, 
  {x:60, y:10}, 
  {x:60, y:80}, 
  {x:10, y:80}
  ];


function printMatrix(mat) {
  mat.forEach(m => document.write(`<br/>&nbsp;&nbsp;${m.join(' ')}`)) 
}
function matrixDot(A, B) {
  /* source:
  https://stackoverflow.com/a/48694670
  */
  var result = new Array(A.length).fill(0).map(row => new Array(B[0].length).fill(0));

  return result.map((row, i) => {
      return row.map((val, j) => {
          return A[i].reduce((sum, elm, k) => sum + (elm*B[k][j]) ,0)
          })
      })
}


function shapeTransform(scaleX, shearX, shiftX,
                        shearY, scaleY, shiftY,
                        pts) {
  let mat = [ [scaleX, shearX, shiftX,],
              [shearY, scaleY, shiftY,] ];
  let vec = [];
  let transformed = [];
  for (let i=0; i<pts.length; i++) {
    vec = [ [pts[i].x],
            [pts[i].y],
            [1] ];
    let res = matrixDot(mat, vec)
    transformed.push({x: res[0], y: res[1]});
  }

  return transformed
}


function applyTransform(){
  scaleX = document.getElementById("scaleX").value;
  shearX = document.getElementById("shearX").value;
  shiftX = document.getElementById("shiftX").value;
  scaleY = document.getElementById("scaleY").value;
  shearY = document.getElementById("shearY").value;
  shiftY = document.getElementById("shiftY").value;

  let transformed = shapeTransform(
    scaleX, shearX, shiftX,
    shearY, scaleY, shiftY,
    corners
  );

  drawPolygon(transformed, 3, "blue");
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawPolygon(corners, 3, "red");
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
