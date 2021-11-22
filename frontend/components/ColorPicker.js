import React from "react";
import { connect } from "react-redux";
import { SketchPicker } from 'react-color';

import { setLedStatus } from "../redux/actions/ledStatusActions";

class ColorPicker extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            showColorPicker: false
        };
    }

    handleChangeComplete = (color) => {
        this.props.setLedStatus("color", color.hex.replace('#',''))
    };

    handleRandomButtonClick = () => {
        this.setState({
            showColorPicker: false
        });
        this.props.setLedStatus("color", "")
    };

    handleSelectButtonClick = () => {
        this.setState({
            showColorPicker: true
        });
    };

    isEnabled = () => {
        return this.props.isVisible || this.state.showColorPicker;
    }

    render() {
        return <div>
                    <label>Color</label>
                    <div className="color-picker-controls">
                        <button onClick={ this.handleSelectButtonClick }>Select</button>
                        <button onClick={ this.handleRandomButtonClick }>Random</button>
                    </div>
                    <div className="color-picker-container" style={{ "visibility": this.isEnabled() ? "visible" : "hidden" }} >
                        <SketchPicker
                            display={ this.isEnabled() }
                            color={ this.props.color }
                            disableAlpha={ true }
                            position="center"
                            width="auto"
                            height="350"
                            onChangeComplete={ this.handleChangeComplete }
                        />
                    </div>
        </div>;
    }
}

const mapStateToProps = state => {
    const { ledStatus } = state;
    const isEnabled = typeof(ledStatus.color) !== "undefined"
    const color = isEnabled ?
        "#"+ledStatus.color : "#0000FF"
    return { color, isVisible: !isEnabled};
};

export default connect(
    mapStateToProps,
    { setLedStatus }
)(ColorPicker);