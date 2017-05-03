/**
 * Created by kasajei on 2017/04/03.
 */
import { takeLatest } from 'redux-saga'
import API from '../Services/Api'
import { BooksTypes } from '../Redux/BooksRedux'
import { searchBooks, amazonBooks } from './BooksSagas'

const api = API.create();

export default function * root () {
  yield [
    takeLatest(BooksTypes.SEARCH_REQUEST, searchBooks, api),
    takeLatest(BooksTypes.AMAZON_REQUEST, amazonBooks, api)
  ]
}
