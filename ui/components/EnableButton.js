import React from "react";
import { connect } from "react-redux";

import { setLedStatus } from "../redux/actions/ledStatusActions";

const getClassName = function(status) {
    var className = "button ";
    if (status!== null) {
        className += status ? "on" : "off";
    }
    else {
        className += "disabled";
    }
    return className;
}

const EnableButton = ({ status, setLedStatus }) => (
    <div className={getClassName(status)} onClick={() => {
        setLedStatus({key: "isOn", value: !status})
    }}
    ></div>
);

const mapStateToProps = function(state) {
    const { ledStatus } = state;
    return { status: ledStatus.isOn };
} 

export default connect(
    mapStateToProps,
    { setLedStatus }
)(EnableButton);