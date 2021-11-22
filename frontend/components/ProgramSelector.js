import React from "react";
import { connect } from "react-redux";
import Select from 'react-select'

import { setLedStatus } from "../redux/actions/ledStatusActions";

const customStyles = {
    control: (base, state) => ({
      ...base,
      background: "white",
      // match with the menu
      borderRadius: state.isFocused ? "3px 3px 0 0" : 3,
      // Overwrittes the different states of border
      borderColor: state.isFocused ? "yellow" : "green",
      // Removes weird border around container
      boxShadow: state.isFocused ? null : null,
      "&:hover": {
        // Overwrittes the different states of border
        borderColor: state.isFocused ? "red" : "blue"
      }
    }),
    menu: base => ({
      ...base,
      // override border radius to match the box
      borderRadius: 0,
      // kill the gap
      marginTop: 0,
    }),
    menuList: base => ({
      ...base,
      // kill the white space on first and last option
      padding: 0,
      background: "#023950"
    }),
};

const ProgramSelector = ({ options, currentMode, setStatus })=> ( 
    <div>
      <label>Led Program</label>
      <Select
          isSearchable={false}
          value={currentMode}
          options={options}
          styles={customStyles}
          onChange={(e) => setStatus("mode", e.value)}
      />
    </div>
)

const mapStateToProps = function(state, props) {
    const { ledStatus, layoutSettings } = state;
    const options = [];

    if (layoutSettings.modes) {
        layoutSettings.modes.forEach(mode => {
            options.push({ value: mode.id, label: mode.name })
        });
    }

    return { 
        options,
        currentMode: options.find(m => m.value === ledStatus.mode)
    };
} 

const mapDispatchToProps = dispatch => {
  return {
    setStatus: (key, value) => {
      dispatch(setLedStatus(key, value))
    }
  }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(ProgramSelector);