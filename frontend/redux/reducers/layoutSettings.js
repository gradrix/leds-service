import { GET_LAYOUT_REQUEST, GET_LAYOUT_SUCCESS } from "../actionTypes";

const initialState = {
  modeIndex: -1,
  modes: [],
  minSpeed: 0,
  maxSpeed: 0,
};

const layoutSettings = (state = initialState, action) => {
  switch (action.type) {
    case GET_LAYOUT_REQUEST:
      return state;
    case GET_LAYOUT_SUCCESS: 
      const result = action.payload;
      return {
        ...state,
        modeIndex: result.modeId,
        modes: result.modes,
        minSpeed: result.minSpeed,
        maxSpeed: result.maxSpeed,
      };
    default:
      return state;
  }
}
  
export default layoutSettings;