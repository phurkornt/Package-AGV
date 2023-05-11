

const rosnodejs = require('rosnodejs');
const std_msgs = rosnodejs.require('std_msgs').msg;

const init_node = "/nodejs_manage"
function send_data(obj) {
    // msg.data = '{ \"topic\":\"map\" , \"script\":\"roslaunch map.launch\" , \"mode\":\"start\"   }'
    const myJSON = JSON.stringify(obj);
    rosnodejs.initNode(init_node)
    .then((rosNode) => {
        let pub = rosNode.advertise('/roboAC/manager_node', std_msgs.String);
        const msg = new std_msgs.String();
        msg.data = myJSON
        pub.publish(msg);
        rosnodejs.log.info('I said: [' + msg.data + ']');
    });
}


function send_nav_data(obj) {
   const myJSON = JSON.stringify(obj);
   rosnodejs.initNode(init_node)
   .then((rosNode) => {
       let pub = rosNode.advertise('/roboAC/nav_node', std_msgs.String);
       const msg = new std_msgs.String();
       msg.data = myJSON
       pub.publish(msg);
       rosnodejs.log.info('I said: [' + msg.data + ']');
   });
}



function test_send_data() {
    rosnodejs.initNode(init_node)
    .then((rosNode) => {
        let pub = rosNode.advertise('/roboAC/manager_node', std_msgs.String);
        const msg = new std_msgs.String();
        msg.data = '{  \"mode\":\"test_status\"   }'
        pub.publish(msg);
    });
}
function test_send_nav_data() {
    rosnodejs.initNode(init_node)
    .then((rosNode) => {
        let pub = rosNode.advertise('/roboAC/nav_node', std_msgs.String);
        const msg = new std_msgs.String();
        msg.data = '{  \"mode\":\"test_status\"   }'
        pub.publish(msg);
    });
}


module.exports.send_data = send_data
module.exports.send_nav_data = send_nav_data

module.exports.test_send_data = test_send_data
module.exports.test_send_nav_data = test_send_nav_data