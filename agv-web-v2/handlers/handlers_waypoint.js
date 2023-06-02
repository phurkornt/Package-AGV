const ip = require('../config/ip');
const activity_state = require('../config/activity_manage');
const node_manager = require('../config/node_manager');

const fs = require('fs');
const path = require('path')

map_path = path.join(__dirname , '..' ,'data','waypoint')

// for embed variable !!
let embed_mapName=''
let embed_plan_name=''



exports.waypoint = (req, res) => {
    let map_files = fs.readdirSync(map_path);
    console.log(activity_state.getData() , map_files);
    
    let plan_waypoint;

    if(embed_mapName!=''){
        let data = fs.readFileSync(`${map_path}/${embed_mapName}.json`);
        plan_waypoint = JSON.parse(data).plan[embed_plan_name];
        console.log(plan_waypoint);
    }

    res.render('main_page',{
        page:"page_waypoint",
        map_files:map_files,
        activity_state:activity_state.getData(),
        my_ip:ip.address,
        embed_mapName:embed_mapName,
        embed_plan_name:embed_plan_name,
        plan_waypoint:plan_waypoint,
        title:"Create Waypoint"
    });
};

// open { mode: 'open', map_name: 'Tetsna2', plan_name: 'hello' }
exports.waypoint_config = (req, res) => {
    console.log("open",req.query);
    let status = activity_state.getData().status;
    let mode = req.query.mode;
    let outData = 'Error'
    switch(mode){
        case 'open':
            if( status == 0){
                // console.log(req.query);
                // save plan , map name -> to use later
                embed_mapName=req.query.map_name
                embed_plan_name=req.query.plan_name

                node_manager.send_data({
                    topic:"slam",
                    script:`rosrun map_server map_server /home/paul/agv/src/roboAC/manager/map/${embed_mapName}.yaml`,
                    mode:"start"
                });
                activity_state.writeData(2);
                outData = 'OK'
            }
            break        
        case 'save':
            // parse two data
            let myObj_waypoint = JSON.parse(req.query.waypoint);
            let myObj_chargepoint = JSON.parse(req.query.chargepoint);

            // console.log("TEST1 " , myObj_waypoint);
            // console.log("TEST2 " , myObj_chargepoint);

            // read file with path and mapName
            let data = fs.readFileSync(`${map_path}/${embed_mapName}.json`);
            let myData = JSON.parse(data);
            // myData = Object(myData);
            
            
            // embed data in myData that use to read
            myData.plan[embed_plan_name]= {}
            myData.plan[embed_plan_name].waypoint = myObj_waypoint
            myData.plan[embed_plan_name].chargepoint = myObj_chargepoint


            // // write some data
            const jsonString = JSON.stringify(myData);
            fs.writeFileSync(`${map_path}/${embed_mapName}.json`, jsonString);

            outData = 'OK'
            break        
        case 'close':

            node_manager.send_data({
                topic:"slam",
                mode:"stop"
            });
            
            activity_state.writeData(0);
            
            // Reset embed data
            embed_mapName=''
            embed_plan_name=''
            
            outData = 'OK'
            break        
        case 'getPlan':
            
            let obj;
            try{
                let data = fs.readFileSync(`${map_path}/${req.query.map_name}.json`);
                obj = JSON.parse(data);
            }catch (err) {
                outData = 'Error'
            }

            console.log(obj);
            outData = obj
            break        
    }
    res.send(outData);
};
