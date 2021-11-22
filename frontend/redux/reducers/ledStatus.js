import { GET_STATUS_REQUEST, GET_STATUS_SUCCESS } from "../actionTypes";

const initialState = {
    isOn: null,
    brightness: 0,
    mode: 0,
    toggle: 0,
    speed: 0,
    color: null,
    lastUpdateTime: null
};

const ledStatus = (state = initialState, action) => {
  switch (action.type) {
    case GET_STATUS_REQUEST:
      return state;
    case GET_STATUS_SUCCESS: 
      const result = action.payload;
      return {
        ...state,
        isOn: result.isOn,
        brightness: result.brightness,
        mode: result.mode,
        toggle: result.toggle,
        speed: result.speed,
        color: result.color ? result.color : null,
        lastUpdateTime: new Date()
      };
    default:
      return {
        ...state,
        isOn: null
      };
  }
}
  
export default ledStatus;