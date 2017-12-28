/**
 * Created by kasajei on 2017/05/12.
 */
import { call, put } from 'redux-saga/effects'
import RecentActions from '../Redux/RecentRedux'


export function * recentBookRelations (api, action) {
  const {sort_id, num, is_manage} = action;
  const response = yield call(api.recent, sort_id, num, is_manage);

  if (response.ok) {
    const {book_relations, last_sort_id} = response.data;
    yield put(RecentActions.recentSuccess(book_relations, last_sort_id));
  } else {
    yield put(RecentActions.requestFailure());
  }
}

export function * recentBookSeen (api, action) {
  const {sort_id} = action;
  const response = yield call(api.seen, sort_id);

  if (response.ok) {
    yield put(RecentActions.seenSuccess());
  } else {
    yield put(RecentActions.requestFailure());
  }
}
