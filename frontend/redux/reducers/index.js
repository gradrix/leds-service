import { combineReducers } from "redux";
import ledStatus from "./ledStatus";
import layoutSettings from "./layoutSettings";

export default combineReducers({ ledStatus, layoutSettings });