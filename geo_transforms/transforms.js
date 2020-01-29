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


//var a = [[-2, 3], [2, 4], [3, 6]]
//var b = [[1, 2, 3], [4, 6, 8]]
////print(matrixDot(a,b));
//printMatrix(matrixDot(a,b));

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

function scaleTransform(scale, pts) {
  let mat = [ [scale.x, 0, 0],
              [0, scale.y , 0] ];
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
function shearTransform(shear, pts) {
  let mat = [ [1, shear, 0],
              [0, 1 , 0] ];
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
  let scaleAmount = {x: document.getElementById("scaleX").value,
                    y: document.getElementById("scaleY").value};
  let shearAmount = document.getElementById("shearInput").value;
  let scaled = scaleTransform(scaleAmount, corners);
  let transformed = shearTransform(shearAmount, scaled);
  drawPolygon(transformed, 5, "blue");
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
