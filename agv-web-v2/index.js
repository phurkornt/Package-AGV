
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');



const app = express();

app.set('view engine', 'ejs');
app.set('views', 'views');

app.use(bodyParser.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')))

// app.use('/admin', express.static(path.join(__dirname, 'public')))
// app.use('/emp', express.static(path.join(__dirname, 'public')))

app.use("/axios",express.static('node_modules/axios/dist'));
app.use("/sweetalert2",express.static('node_modules/sweetalert2/dist'));

app.use(session({
    secret:'secret',
    resave:false,
    saveUninitialized:false
}))

const routes = require('./routes/routes');
app.use('/',routes);



//----------------------- init -----------------------

const activity_state = require('./config/activity_manage');
const test_manage = require('./config/node_manager')
test_manage.test_send_data();
test_manage.test_send_nav_data();

activity_state.writeData(0)

// console.log(activity_state.getData())

//----------------------- init -----------------------


port = 3000

app.listen(port,()=>{
    console.log(`Server run at port : ${port}`)
});