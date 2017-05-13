/**
 * Created by kasajei on 2017/05/12.
 */
import { call, put } from 'redux-saga/effects'
import RecentActions from '../Redux/RecentRedux'


export function * recentBookRelations (api, action) {
  const {sort_id, num} = action;
  const response = yield call(api.recent, sort_id, num);

  if (response.ok) {
    const {book_relations, last_sort_id} = response.data;
    yield put(RecentActions.recentSuccess(book_relations, last_sort_id));
  } else {
    yield put(RecentActions.requestFailure());
  }
}
