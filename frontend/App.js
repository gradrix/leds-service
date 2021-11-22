import React from "react";
import { connect } from 'react-redux';

import { fetchLedStatus } from "./redux/actions/ledStatusActions";
import { fetchLayoutSettings } from "./redux/actions/layoutSettingsActions";
import StatusContainer from './components/StatusContainer';
import SliderContainer from "./components/SliderContainer";
import ProgramSelector from "./components/ProgramSelector";
import ColorPicker from "./components/ColorPicker";
import './App.scss';

class App extends React.Component {

  getLedStatus() {
    this.updateModeLayoutIfNeeded();
    this.props.fetchLedStatus();
  }

  updateModeLayoutIfNeeded() {
    if (this.props.currentMode !== this.props.mode) {
      this.props.fetchLayoutSettings();
    }
  };

  componentDidMount() {
    this.getLedStatus();

    this.timerId = setInterval(
      () => this.getLedStatus(),
      5000
    );
  };

  componentWillUnmount() {
    clearInterval(this.timerId);
  };
 
  render() {
    return (
      <div className="LedsApp">
        <header className="App-header">
          <h1 className="App-title">{this.props.modeName} Control</h1>
        </header>
        <StatusContainer />
        <SliderContainer label="Brightness" settingKey="brightness" />
        <SliderContainer label="Speed" settingKey="speed" min={this.props.minSpeed} max={this.props.maxSpeed}/>
        <br/>
        <ProgramSelector />
        <br/>
        <ColorPicker />
    </div>
    );
  };
}

const mapStateToProps = state => {
  const { ledStatus, layoutSettings } = state;
  
  const ledProgram = layoutSettings.modes.find(m => m.id === ledStatus.mode)

  return { 
    isOn: ledStatus.isOn,
    modeName: ledProgram ? ledProgram.name : "Led",
    currentMode: ledStatus.mode,
    mode: layoutSettings.modeIndex,
    minSpeed: layoutSettings.minSpeed, 
    maxSpeed: layoutSettings.maxSpeed 
  };
};

export default connect(
  mapStateToProps,
  { fetchLedStatus, fetchLayoutSettings }
)(App);
