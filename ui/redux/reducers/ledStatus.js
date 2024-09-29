import { 
  GET_STATUS_REQUEST, 
  GET_STATUS_SUCCESS, 
  GET_LAYOUT_REQUEST,
  GET_LAYOUT_SUCCESS,
  SET_SERVICE_REQUEST,
  SET_SERVICE_SUCCESS
} from "../actionTypes";

const initialState = {
    isOn: null,
    brightness: 0,
    mode: 0,
    toggle: 0,
    speed: 0,
    color: null,
    lastUpdateTime: null
};
let previousState = initialState;

const ledStatus = (state = initialState, action) => {
  switch (action.type) {
    case GET_STATUS_REQUEST:
      previousState = state;
      return state;
    case GET_STATUS_SUCCESS: 
      const result = action.payload;
      const newState = {
        ...state,
        isOn: result.isOn,
        brightness: result.brightness,
        mode: result.mode,
        toggle: result.toggle,
        speed: result.speed,
        color: result.color ? result.color : null,
        lastUpdateTime: new Date()
      };
      previousState = newState;
      return newState;
    case GET_LAYOUT_REQUEST:
    case GET_LAYOUT_SUCCESS:
    case SET_SERVICE_REQUEST:
    case SET_SERVICE_SUCCESS:
      return previousState;
    default:
      return {
        ...previousState,
        isOn: null
      };
  }
}
  
export default ledStatus;