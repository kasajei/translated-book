/**
 * Created by kasajei on 2017/04/03.
 */
import { combineReducers } from 'redux'
import configureStore from './CreateStore'
import rootSaga from '../Sagas/index'
import { syncHistoryWithStore, routerReducer } from 'react-router-redux'

export default () => {
  const rootReducer = combineReducers({
    routing: routerReducer,
    booking: require('./BooksRedux').reducer,
    recenting: require('./RecentRedux').reducer,
  });

  return configureStore(rootReducer, rootSaga)
}
