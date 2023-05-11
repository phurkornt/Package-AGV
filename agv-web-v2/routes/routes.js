
const express = require('express');

const slam_handlers= require('../handlers/handlers_slam')
const route_handlers= require('../handlers/handlers_route')
const waypoint_handlers= require('../handlers/handlers_waypoint')
const navigation_handlers= require('../handlers/handlers_navigation')

const router = express.Router();


router.get('/', route_handlers.route);

router.get('/slam', slam_handlers.slam);
router.get('/slam_config', slam_handlers.slam_config);

router.get('/waypoint', waypoint_handlers.waypoint);
router.get('/waypoint_config', waypoint_handlers.waypoint_config);


router.get('/navigation', navigation_handlers.navigation);
router.get('/navigation_config', navigation_handlers.navigation_config);
router.get('/navigation_nav', navigation_handlers.navigation_nav);


module.exports = router;
