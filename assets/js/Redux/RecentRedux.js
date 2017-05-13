/**
 * Created by kasajei on 2017/04/03.
 */
import { createReducer, createActions } from 'reduxsauce'
import Immutable from 'seamless-immutable'


const { Types, Creators } = createActions({
  recentRequest: ["sort_id", "num"],
  recentSuccess:['book_relations', 'last_sort_id'],
  requestFailure: null
});

export const RecentTypes = Types;
export default Creators;

export const INITIAL_STATE = Immutable({
  recent_book_relations: [],
  last_sort_id: null,
  fetching: false,
  error: null,
});


export const recentRequest = (state, {sort_id, num}) =>
  state.merge({ recent_book_relations: [], last_sort_id:null, fetching:true });

export const recentSuccess = (state, action) => {
  const { book_relations, last_sort_id } = action;
  const {recent_book_relations} = state;
  return state.merge({ recent_book_relations: recent_book_relations.concat(book_relations),fetching:false, last_sort_id});
};

// failed to get the temperature
export const requestFailure = (state) =>
  state.merge({ fetching: false, error: true});


export const reducer = createReducer(INITIAL_STATE, {
  [Types.RECENT_RQUEST]: recentRequest,
  [Types.RECENT_SUCCESS]: recentSuccess,
  [Types.REQUEST_FAILURE]: requestFailure,
});
