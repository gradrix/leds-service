import React from "react";
import { connect } from "react-redux";

import Clock from "./Clock";
import EnableButton from "./EnableButton";

const StatusContainer = ({ status, stateText }) => (
    <div className="led-status">
        <div className="text">
            <div className="status">Status: <span className={status}>{stateText}</span></div>
            <Clock />
        </div>
        <EnableButton />
    </div>  
);

const mapStateToProps = function(state) {
    const { ledStatus } = state;
    
    let status = "inactive";
    let stateText = "Off (offline)";   

    if (ledStatus.isOn !== null) {
        status = ledStatus.isOn ? "active": "inactive";
        stateText = ledStatus.isOn ? "On": "Off";
    }
    return { status, stateText };
} 

export default connect(
    mapStateToProps,
)(StatusContainer);