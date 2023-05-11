
const fs = require('fs');
const path = require('path')

my_file = path.join(__dirname,'..','data') + '/activity.json'

function getData(){
    try {
        var data = fs.readFileSync(my_file);
        var obj = JSON.parse(data);
    } catch (err) {
        console.error(err);
    }

    return obj;
}

function condition_act(status){
    activity = ''
    switch(status){
        case 0: 
            activity = 'free'
            break;
        case 1: 
            activity = 'slam'
            break;
        case 2: 
            activity = 'waypoint'
            break;
        case 3: 
            activity = 'navigation'
            break;
    }
    return activity
}

function writeData(status){
    const obj = { 
        activity: condition_act(status), 
        status: status
    };
    try {
        const jsonString = JSON.stringify(obj);
        fs.writeFileSync(my_file, jsonString);
        console.log('Write JSON file successfully');
      } catch (err) {
        console.error(err);
      }
}



module.exports.getData = getData;
module.exports.writeData = writeData;