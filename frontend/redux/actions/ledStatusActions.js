import { GET_STATUS_REQUEST, GET_STATUS_SUCCESS, GET_STATUS_ERROR } from "../actionTypes";

export const getStatusRequest = () => ({
    type: GET_STATUS_REQUEST
});

export const getStatusSuccess = payload => ({
    type: GET_STATUS_SUCCESS,
    payload
});

export const getStatusError = () => ({
    type: GET_STATUS_ERROR
});

let isRequestRunning = false;

const processStatusResponse = function(dispatch, response, json) {
    isRequestRunning = false;
    if (response.status === 200) {
        dispatch(getStatusSuccess(json));
    }
    else {
        dispatch(getStatusError());
    }
}

export const fetchLedStatus = function() {
    return (dispatch) => {

        if (isRequestRunning) return;
        isRequestRunning = true;

        return fetch("/api/status/", { method: 'GET'})
            .then(response => Promise.all([response, response.json()]))
            .then(([response, json]) => 
                processStatusResponse(dispatch, response, json)
            ).catch(function(error) {
                isRequestRunning = false;
                dispatch(getStatusError())
            });
    }
}

export const setLedStatus = function(key, value) {
    return (dispatch) => {

        dispatch(getStatusRequest());
        if (isRequestRunning) return;

        isRequestRunning = true;

        var objToSend = {}
        objToSend["key"] = key;
        objToSend["value"] = value;
    
        return fetch("/api/changestatus/", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(objToSend)
        })
        .then(response => Promise.all([response, response.json()]))
        .then(([response, json]) => 
            processStatusResponse(dispatch, response, json)
        ).catch(function(error) {
            isRequestRunning = false;
            dispatch(getStatusError())
        }); 
    }
}