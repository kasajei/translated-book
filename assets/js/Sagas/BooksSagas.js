/**
 * Created by kasajei on 2017/04/03.
 */
import { call, put } from 'redux-saga/effects'
import BooksActions from '../Redux/BooksRedux'

export function * searchBooks (api, action) {
  const response = yield call(api.search);

  if (response.ok) {
    const books = response.data.books;
    yield put(BooksActions.searchSuccess(books));
  } else {
    yield put(BooksActions.requestFailure());
  }
}
