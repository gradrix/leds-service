import React from "react";
import { connect } from "react-redux";
import ReactSlider from 'react-slider'
import styled from 'styled-components';

import { setLedStatus } from "../redux/actions/ledStatusActions";
/*
Styling
*/
const StyledSlider = styled(ReactSlider)`
    width: 100%;
    height: 25px;
`;

const StyledThumb = styled.div`
    height: 25px;
    line-height: 25px;
    width: 25px;
    text-align: center;
    background-color: #000;
    color: #fff;
    border-radius: 50%;
    cursor: grab;
`;

const StyledTrack = styled.div`
    top: 0;
    bottom: 0;
    background: ${props => props.index === 2 ? '#f00' : props.index === 1 ? '#eaabab' : '#6fd46f'};
    border-radius: 999px;
`;
/*
Styling End
*/

const Thumb = (props, state) => <StyledThumb {...props}>{state.valueNow}</StyledThumb>;

const Track = (props, state) => <StyledTrack {...props} index={state.index} />;

const SliderContainer = (props) => (
    <div className="slider-container">
        <label>{props.label}: {props.value}</label>
        <StyledSlider
            renderTrack={Track}
            renderThumb={Thumb}
            min={(props.min ? props.min : 0)}
            max={(props.max ? props.max : 100)}
            value={props.value}
            onAfterChange={newValue => props.setLedStatus(props.settingKey, newValue)}
        />
    </div>
);

const mapStateToProps = function(state, props) {
    const { ledStatus } = state;
    return { value: ledStatus[props.settingKey] };
} 

export default connect(
    mapStateToProps,
    { setLedStatus }
)(SliderContainer);