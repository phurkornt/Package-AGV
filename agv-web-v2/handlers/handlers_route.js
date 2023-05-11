const ip = require('../config/ip');
const activity_state = require('../config/activity_manage');


exports.route = (req, res) => {
    console.log(activity_state.getData());
    res.render('main_page',{
        page:"page_routes",
        activity_state:activity_state.getData(),
        my_ip:ip.address
    });
};