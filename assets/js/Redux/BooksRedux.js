/**
 * Created by kasajei on 2017/04/03.
 */
import { createReducer, createActions } from 'reduxsauce'
import Immutable from 'seamless-immutable'


const { Types, Creators } = createActions({
  searchRequest: ["isbn", "title", "author"],
  selectBook: ["book"],
  searchSuccess: ['books'],
  amazonRequest: ["title", "original_title"],
  amazonSuccess: ["original_book", "translated_book", 'other_books'],
  requestFailure: null
});

export const BooksTypes = Types;
export default Creators;

export const INITIAL_STATE = Immutable({
  books: [],
  selected_book: null,
  original_book: null,
  translated_book: null,
  other_books: [],
  fetching: null,
  error: null,
});

export const searchRequest = (state, {isbn, title, author}) =>
  state.merge({ fetching: true, books: [], original_book:null, translated_book:null, other_books:[]});

export const selectBook = (state, {book}) => {
  return state.merge({selected_book: book});
};

// successful temperature lookup
export const searchSuccess = (state, action) => {
  const { books } = action;
  return state.merge({ fetching: false, error: null, books });
};

export const amazonRequest = (state, {title, original_title}) =>
  state.merge({ fetching: true, original_book:null, translated_book:null, other_books:[]});

export const amazonSuccess = (state, action) => {
  const { original_book, translated_book, other_books } = action;
  return state.merge({ fetching: false, error: null, original_book, translated_book, other_books });
};


// failed to get the temperature
export const requestFailure = (state) =>
  state.merge({ fetching: false, error: true, books: [] ,original_book:null, translated_book:null, other_books:[]});


export const reducer = createReducer(INITIAL_STATE, {
  [Types.SEARCH_REQUEST]: searchRequest,
  [Types.SELECT_BOOK]: selectBook,
  [Types.SEARCH_SUCCESS]: searchSuccess,
  [Types.REQUEST_FAILURE]: requestFailure,
  [Types.AMAZON_REQUEST]: amazonRequest,
  [Types.AMAZON_SUCCESS]: amazonSuccess,
});
