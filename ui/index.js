import React from "react";
import ReactDOM from 'react-dom';
import { Provider } from "react-redux";

import store from "./redux/store";
import LedsClient from './LedsClient';
import './css/LedsClient.scss';

const appElement = document.getElementById("LedsClient");
ReactDOM.render(
  <Provider store={store}>
    <LedsClient services={1} />
  </Provider>,
  appElement
);
