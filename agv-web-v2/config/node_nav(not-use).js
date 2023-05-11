

const rosnodejs = require('rosnodejs');
const std_msgs = rosnodejs.require('std_msgs').msg;


function send_data(obj) {
    // msg.data = '{ \"topic\":\"map\" , \"script\":\"roslaunch map.launch\" , \"mode\":\"start\"   }'
    const myJSON = JSON.stringify(obj);
    rosnodejs.initNode('/nodejs_manage')
    .then((rosNode) => {
        let pub = rosNode.advertise('/roboAC/nav_node', std_msgs.String);
        const msg = new std_msgs.String();
        msg.data = myJSON
        pub.publish(msg);
        rosnodejs.log.info('I said: [' + msg.data + ']');
    });
}

function test_send_data() {
    rosnodejs.initNode('/nodejs_manage')
    .then((rosNode) => {
        let pub = rosNode.advertise('/roboAC/nav_node', std_msgs.String);
        const msg = new std_msgs.String();
        msg.data = '{  \"mode\":\"test_status\"   }'
        pub.publish(msg);
    });
}

module.exports.send_data = send_data
module.exports.test_send_data = test_send_data