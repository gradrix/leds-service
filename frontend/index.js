import React from "react";
import ReactDOM from 'react-dom';
import { Provider } from "react-redux";

import store from "./redux/store";
import App from './App';

const appElement = document.getElementById("App");
ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  appElement
);