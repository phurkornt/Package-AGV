const ip = require('../config/ip');
const activity_state = require('../config/activity_manage');
const node_manager = require('../config/node_manager');

const fs = require('fs');
const path = require('path')



map_path = path.join(__dirname , '..' ,'data','waypoint')

// for embed variable !!
let embed_mapName=''
let embed_plan_name=''

exports.navigation = (req, res) => {
    let map_files = fs.readdirSync(map_path);
    let plan_waypoint;


    if(embed_mapName!=''){
        let data = fs.readFileSync(`${map_path}/${embed_mapName}.json`);

        if( embed_plan_name != ""){
            plan_waypoint = JSON.parse(data).plan[embed_plan_name];
        }else{
            plan_waypoint = JSON.parse(data);
        }
        
        console.log(plan_waypoint);
    }


    res.render('main_page',{
        page:"page_navigation",
        activity_state:activity_state.getData(),
        my_ip:ip.address,
        map_files:map_files,
        embed_mapName:embed_mapName,
        embed_plan_name:embed_plan_name,
        plan_waypoint:plan_waypoint,
        title:"Navigation"
    });
};

exports.navigation_config = (req, res) => {
    console.log("open",req.query);
    let status = activity_state.getData().status;
    let mode = req.query.mode;
    let outData = 'Error'
    switch(mode){
        case 'open':
            if( status == 0){
                embed_mapName=req.query.map_name
                // Run map & navaigation

                // node_manager.send_data({
                //     topic:"navigation",
                //     script:`roslaunch turtlebot3_navigation turtlebot3_navigation.launch`,
                //     mode:"start"
                // });
                setTimeout(() => {
                    node_manager.send_data({
                        topic:"navigation1",
                        script:`roslaunch turtlebot3_navigation turtlebot3_navigation.launch`,
                        mode:"start"
                    });
                }, 1000);
                setTimeout(() => {
                    node_manager.send_data({
                        topic:"nav_map",
                        script:`rosrun map_server map_server /home/paul/agv/src/roboAC/manager/map/${embed_mapName}.yaml`,
                        mode:"start"
                    });
                }, 500);
                activity_state.writeData(3);
                outData = 'OK'
            }
            break        
        case 'run_plan':
            embed_plan_name=req.query.plan_name

            // Send plan to node_nav
            let data = fs.readFileSync(`${map_path}/${embed_mapName}.json`);
            plan_waypoint = JSON.parse(data).plan[embed_plan_name];

            node_manager.send_nav_data({
                mode:"set",
                waypoint:plan_waypoint.waypoint,
                chargepoint:plan_waypoint.chargepoint
            })

            outData = 'OK'
            break        
        case 'close':
            
            node_manager.send_data({
                topic:"nav_map",
                mode:"stop"
            });
            
            activity_state.writeData(0);
            embed_mapName=''
            embed_plan_name=''
            outData = 'OK'
            break        
        case 'get_back':
            embed_plan_name=''
            outData = 'OK'
            break        
    }
    res.send(outData);
};


exports.navigation_nav = (req, res) => {
    switch(req.query.mode){
        case "set":
            let data = fs.readFileSync(`${map_path}/${embed_mapName}.json`);
            plan_waypoint = JSON.parse(data).plan[embed_plan_name];
            console.log("DEBUG ->",plan_waypoint);
            node_manager.send_nav_data({
                mode:"set",
                waypoint:plan_waypoint.waypoint,
                chargepoint:plan_waypoint.chargepoint
            })
        break
        case "sw":
            node_manager.send_nav_data({
                mode:"sw"
            })
        break
        case "pause":
            node_manager.send_nav_data({
                mode:"pause"
            })
        break
        case "run":
            node_manager.send_nav_data({
                mode:"run"
            })
        break
    }
    res.send("OK")
    
};