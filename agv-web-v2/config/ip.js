const os = require('os');

const interfaces = os.networkInterfaces();
const addresses = [];

for (const name of Object.keys(interfaces)) {
  for (const iface of interfaces[name]) {
    // เฉพาะ IPv4 และไม่ใช่เครือข่าย loopback
    if (iface.family === 'IPv4' && !iface.internal) {
      addresses.push(iface.address);
    }
  }
}

robot_address = addresses.length == 0 ? '127.0.0.1' : addresses[0]
console.log(robot_address);
module.exports.address = robot_address
