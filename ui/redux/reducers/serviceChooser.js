import { SET_SERVICE_REQUEST, SET_SERVICE_SUCCESS } from "../actionTypes";

const initialState = {
    serviceIndex: 1
};
let previousState;

const serviceChooser = (state = initialState, action) => {
    switch (action.type) {
      case SET_SERVICE_REQUEST:
        previousState = state;
        return state;
      case SET_SERVICE_SUCCESS: 
        const result = action.payload;
        const newState = {
          serviceIndex: result.serviceIndex
        };
        previousState = newState;
        return newState;
      default:
        return state;
    }
  }

  export default serviceChooser;