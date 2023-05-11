const fs = require('fs');
const path = require('path');


mypath = path.join(__dirname , '..' ,'data','waypoint')

let myObj = JSON.parse(`[{"name":"1","pose":{"position":{"x":0,"y":0,"z":0.01},"orientation":{"x":0,"y":0,"z":0,"w":1}}},{"name":"2","pose":{"position":{"x":0,"y":0,"z":0.01},"orientation":{"x":0,"y":0,"z":0,"w":1}}}]`);
console.log(myObj);


const jsonString = '[{"name":"1","pose":{"position":{"x":0,"y":0,"z":0.01},"orientation":{"x":0,"y":0,"z":0,"w":1}}},{"name":"2","pose":{"position":{"x":0,"y":0,"z":0.01},"orientation":{"x":0,"y":0,"z":0,"w":1}}}]';
const obj = JSON.parse(jsonString);

for(let i of obj){
    console.log(i);
}
// console.log(myObj);