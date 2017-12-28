import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import createStore from './Redux/index'
import { Router, Route, browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux'

import MainView from './Containers/MainView';
import RecentBookView from './Containers/RecentBookView';
import BookManageView from './Containers/BookManageView';



const store = createStore();

const history = syncHistoryWithStore(browserHistory, store);

ReactDOM.render(
    <Provider store={store}>
      <Router history={history}>
        <Route exact path="/" component={MainView}/>
        <Route path="/recent" component={RecentBookView}/>
        <Route path="/manage" component={BookManageView}/>
      </Router>
    </Provider>
  , document.getElementById('react-app')
);