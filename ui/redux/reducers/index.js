import { combineReducers } from "redux";
import ledStatus from "./ledStatus";
import layoutSettings from "./layoutSettings";
import serviceChooser from "./serviceChooser";

export default combineReducers({ 
    ledStatus, 
    layoutSettings,
    serviceChooser 
});