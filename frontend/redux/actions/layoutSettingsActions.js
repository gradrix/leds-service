import { GET_LAYOUT_REQUEST, GET_LAYOUT_SUCCESS, GET_LAYOUT_ERROR } from "../actionTypes";

export const getLayoutSettingsRequest = () => ({
    type: GET_LAYOUT_REQUEST
});

export const getLayoutSettingsSuccess = payload => ({
    type: GET_LAYOUT_SUCCESS,
    payload
});

export const getLayoutSettingsError = () => ({
    type: GET_LAYOUT_ERROR
});

let isLayoutRequestRunning = false;

const processLayoutResponse = function(dispatch, response, json) {
    isLayoutRequestRunning = false;
    if (response.status === 200) {
        dispatch(getLayoutSettingsSuccess(json))
    }
    else {
        dispatch(getLayoutSettingsError())
    }
}

export const fetchLayoutSettings = function() {
    return (dispatch) => {

        if (isLayoutRequestRunning) return;

        dispatch(getLayoutSettingsRequest());
        isLayoutRequestRunning = true;

        return fetch("/api/layout/", { method: 'GET'})
        .then(response => Promise.all([response, response.json()]))
        .then(([response, json]) => 
            processLayoutResponse(dispatch, response, json)
        ).catch(function(error) {
            isLayoutRequestRunning = false;
            dispatch(getLayoutSettingsError())
        });
    }
}