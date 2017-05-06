/**
 * Created by kasajei on 2017/04/03.
 */
import { call, put } from 'redux-saga/effects'
import BooksActions from '../Redux/BooksRedux'

export function * searchBooks (api, action) {
  const {isbn, title, author} = action;
  const response = yield call(api.search, isbn, title, author);

  if (response.ok) {
    const books = response.data.books;
    yield put(BooksActions.searchSuccess(books));
  } else {
    yield put(BooksActions.requestFailure());
  }
}

export function * amazonBooks (api, action) {
  const {title, original_title} = action;
  const response = yield call(api.amazon, title, original_title);

  if (response.ok) {
    const original_book = response.data.original_product;
    const translated_book = response.data.translated_product;
    const other_books = response.data.other_books;
    yield put(BooksActions.amazonSuccess(original_book, translated_book, other_books));
  } else {
    yield put(BooksActions.requestFailure());
  }
}
