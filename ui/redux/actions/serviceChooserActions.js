import { SET_SERVICE_REQUEST, SET_SERVICE_SUCCESS } from "../actionTypes";
import { fetchLayoutSettings } from "./layoutSettingsActions";

export const setServiceRequest = () => ({
    type: SET_SERVICE_REQUEST
});

export const setServiceSuccess = payload => ({
    type: SET_SERVICE_SUCCESS,
    payload
});

export const setServiceIndex = function({serviceIndex}) {
    return (dispatch) => {
        dispatch(setServiceRequest());        
        dispatch(setServiceSuccess({serviceIndex}));
        dispatch(fetchLayoutSettings());
    }
}