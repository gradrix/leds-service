import React from "react";
import { connect } from "react-redux";
import Select from 'react-select';
import Cookies from 'universal-cookie';

import { setServiceIndex } from "../redux/actions/serviceChooserActions";
import { programSelectorStyle } from "../css/selectorStyles";

const cookies = new Cookies();

class ServiceSelector extends React.Component {

  render() {
    return <div className="selector">
            <label>Service:</label>
            <Select
                isSearchable={false}
                value={this.props.currentIndex}
                options={this.props.options}
                styles={programSelectorStyle}
                onChange={(e) => this.props.setServiceIndex(e.value)}
            />
          </div>;
  }

  UNSAFE_componentWillMount() {
    const initialValue = this.props.initialValue;
    const cookieValue = cookies.get('serviceIndex')
    const currentIndex = (cookieValue && +cookieValue <= this.props.services && +cookieValue > 0)
      ? +cookieValue
      : initialValue
    if (currentIndex !== this.props.currentIndex.value) {
      this.props.setServiceIndex(currentIndex)
    }
 }
}

const mapStateToProps = function(state, props) {
    const options = [];

    for (let i = 1; i <= props.services; i++) {
      options.push({ value: i, label: "#"+ i +" Led Service" })
    }

    return { 
        options,
        currentIndex: options[state.serviceChooser.serviceIndex - 1],
        initialValue: state.serviceChooser.serviceIndex
    };
} 

const mapDispatchToProps = dispatch => {
  return {
    setServiceIndex: (index) => {
      cookies.set('serviceIndex', index, { path: '/', maxAge: 31536000, sameSite: true });
      dispatch(setServiceIndex({serviceIndex: index}))
    }
  }
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(ServiceSelector);