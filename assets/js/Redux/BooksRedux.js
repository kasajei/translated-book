/**
 * Created by kasajei on 2017/04/03.
 */
import { createReducer, createActions } from 'reduxsauce'
import Immutable from 'seamless-immutable'


const { Types, Creators } = createActions({
  searchRequest: ["isbn", "title", "author"],
  searchSuccess: ['books'],
  amazonRequest: ["title", "original_title"],
  amazonSuccess: ["original_book", "translated_book", 'other_books'],
  requestFailure: null
});

export const BooksTypes = Types;
export default Creators;

export const INITIAL_STATE = Immutable({
  books: [],
  original_book: null,
  translated_book: null,
  other_books: [],
  fetching: null,
  error: null,
});

export const search = (state) =>
  state.merge({ fetching: true, books: [], original_book:null, translated_book:null, other_books:[]});

// successful temperature lookup
export const searchSuccess = (state, action) => {
  const { books } = action;
  return state.merge({ fetching: false, error: null, books });
};

// failed to get the temperature
export const requestFailure = (state) =>
  state.merge({ fetching: false, error: true, books: [] ,original_book:null, translated_book:null, other_books:[]});


export const reducer = createReducer(INITIAL_STATE, {
  [Types.SEARCH_REQUEST]: search,
  [Types.SEARCH_SUCCESS]: searchSuccess,
  [Types.REQUEST_FAILURE]: requestFailure,
});
