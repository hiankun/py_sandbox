"use strict"

var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
ctx.setTransform(1, 0, 0, -1, 0, canvas.height);//flip vertically
ctx.translate(canvas.width/2, canvas.height/2); //shift origin
drawCoord();
var corners = [
  {x:-30, y:-40}, 
  {x:30, y:-40}, 
  {x:30, y:40}, 
  {x:-30, y:40}
  ];
drawPolygon(corners, 2, "red");

function drawCoord() {
  ctx.beginPath();
  ctx.lineWidth = 1;
  ctx.strokeStyle = 'white';
  ctx.moveTo(-canvas.width/2,0);
  ctx.lineTo(canvas.width/2,0);
  ctx.moveTo(0,-canvas.height/2);
  ctx.lineTo(0,canvas.height/2);
  ctx.stroke();
}


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


function rotateOrig(angle, pts) {
  let ang = angle * Math.PI / 180.0
  let mat = [ [Math.cos(ang), -Math.sin(ang), 0.0],
              [Math.sin(ang),  Math.cos(ang), 0.0] ];
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
  rotate = document.getElementById("rotate").value;

  let translated = shapeTransform(
    scaleX, shearX, shiftX,
    shearY, scaleY, shiftY,
    corners
  );

  let transformed = rotateOrig(rotate, translated);

  drawPolygon(transformed, 2, "blue");
}

function clearCanvas() {
  ctx.clearRect(-canvas.width/2, -canvas.height/2, 
                 canvas.width,  canvas.height);
  drawCoord();
  drawPolygon(corners, 2, "red");
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


// the following functions are for test purpose
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
