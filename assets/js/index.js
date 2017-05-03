import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import createStore from './Redux/index'
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux'

import MainView from './Containers/MainView';
import PostView from './Containers/PostView';


const store = createStore();

const history = syncHistoryWithStore(browserHistory, store);

ReactDOM.render(
    <Provider store={store}>
      <Router history={history}>
        <Route exact path="/" component={MainView}/>
        <Route path="/post" component={PostView}/>
      </Router>
    </Provider>
  , document.getElementById('react-app')
);