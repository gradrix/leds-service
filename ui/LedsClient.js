import React from "react";
import { connect } from 'react-redux';

import { fetchLedStatus } from "./redux/actions/ledStatusActions";
import { fetchLayoutSettings } from "./redux/actions/layoutSettingsActions";
import StatusContainer from './components/StatusContainer';
import SliderContainer from "./components/SliderContainer";
import ProgramSelector from "./components/ProgramSelector";
import ColorPicker from "./components/ColorPicker";
import ServiceSelector from "./components/ServiceSelector";

class LedsClient extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      services: props.services || 1 
    }
  }

  componentDidMount() {
    this.props.fetchLayoutSettings();

    this.timerId = setInterval(
      () => this.props.fetchLedStatus(),
      4000
    );
  };

  componentWillUnmount() {
    clearInterval(this.timerId);
  };
 
  render() {
    const serviceContainer = this.state.services > 1 
      ? <ServiceSelector services={this.state.services} />
      : null;
    const service = this.state.services > 1 
      ? "#"+ this.props.service  +" "
      : "";

    return (
      <div className="LedsApp">
        <header className="App-header">
          <h1 className="App-title">{service}{this.props.modeName} Control</h1>
        </header>
        <StatusContainer />
        <div className="settings">
          {serviceContainer} 
          <ProgramSelector />
        </div>        
        <SliderContainer label="Brightness" settingKey="brightness" />
        <SliderContainer label="Speed" settingKey="speed" min={this.props.minSpeed} max={this.props.maxSpeed}/>
        <ColorPicker />
    </div>
    );
  };
}

const mapStateToProps = state => {
  const { ledStatus, layoutSettings, serviceChooser } = state;
  
  const ledProgram = layoutSettings.modes.find(m => m.id === ledStatus.mode)

  return { 
    isOn: ledStatus.isOn,
    modeName: ledProgram ? ledProgram.name : "Led",
    currentMode: ledStatus.mode,
    mode: layoutSettings.modeIndex,
    minSpeed: layoutSettings.minSpeed, 
    maxSpeed: layoutSettings.maxSpeed,
    service:  serviceChooser.serviceIndex
  };
};

export default connect(
  mapStateToProps,
  { fetchLedStatus, fetchLayoutSettings }
)(LedsClient);
