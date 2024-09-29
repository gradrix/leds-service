import React from "react";
import { connect } from "react-redux";
import Select from 'react-select'

import { setLedStatus } from "../redux/actions/ledStatusActions";
import { programSelectorStyle } from "../css/selectorStyles"

class ProgramSelector extends React.Component {

  render() {
    return <div className="selector">
            <label>Led Program:</label>
            <Select
                isSearchable={false}
                value={this.props.currentMode}
                options={this.props.options}
                styles={programSelectorStyle}
                onChange={(e) => this.props.setStatus("mode", e.value)}
            />
          </div>;
  }
}

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
      dispatch(setLedStatus({key, value}))
    }
  }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(ProgramSelector);