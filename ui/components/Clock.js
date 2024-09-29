import React from "react";
import { connect } from "react-redux";
import moment from "moment";

const blankUpdateTime = "-s ago / --:--:--";

class Clock extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            clockText: blankUpdateTime
        };
    }

    getAgoTime = function(seconds) {
        let result = "";
        const secs = seconds % 60;
        const minutes = Math.floor(seconds / 60) % 60;
        const hours = Math.floor(seconds / 3600);
        
        if (hours > 0) {
            result += hours + "h ";
        }
        if (minutes > 0) {
            result += minutes + "m ";
        }
        
        result += secs + "s ago";
        return result;
    }

    getClockText = function() {
        var timeSinceLast = "infinite ";
        if (this.props.updatedAt) {
            timeSinceLast = Math.floor((new Date() - this.props.updatedAt) / 1000);
            return this.getAgoTime(timeSinceLast)+ " / " +moment(this.props.updatedAt).format("HH:mm:ss");
        } 
        return blankUpdateTime;
    }

    tick() {
        if (this.props.updatedAt !== null)
            this.setState({
                clockText: this.getClockText()
            });
    }

    componentDidMount() {
        this.timerId = setInterval(
            () => this.tick(),
            1000
        );
    };

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {
        return (
            <div className="clock">{this.state.clockText}</div>
        )
    }
}

const mapStateToProps = state => {
    const { ledStatus } = state;
    return { updatedAt: ledStatus.lastUpdateTime };
};

export default connect(mapStateToProps)(Clock);