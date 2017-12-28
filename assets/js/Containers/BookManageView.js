import React from 'react';
import {Link} from 'react-router'
import RecentActions from '../Redux/RecentRedux'
import { connect } from 'react-redux'
import Footer from '../Component/Footer'
import Header from '../Component/Header'
import BookRelation from '../Component/BookRelation'


Array.prototype.chunk = function(n){
    var len = Math.round(this.length/n,10);
    var ret = [];
    for(var i=0;i<len;i++){
        ret.push( this.slice( i*n, i*n+n )  )
    }
    return ret;
};


class BookManageView extends React.Component{
  constructor(props){
    super(props);
    this.loadNext = this.loadNext.bind(this);
    this.seenRequests = this.seenRequests.bind(this);
  }
  componentWillMount(){
    if (this.props.recent_book_relations.length === 0) {
      this.props.recentBooks(null, 24)
    }
  }
  renderRecent(){
    return (
      this.props.recent_book_relations.chunk(2).map(function (book_relations) {
      return(
        <div className="columns">
          {
            book_relations.map(function (book_relation) {
              return <BookRelation amazon={book_relation.translated_book} original={book_relation.original_book} key={book_relation.translated_book.asin}/>
            })
          }
        </div>
      )
    })
    )
  }
  loadNext(){
    this.props.recentBooks(this.props.last_sort_id, 24)
  }
  seenRequests(){
    this.props.seenBooks(this.props.last_sort_id)
  }
  renderNext(){
    if(this.props.last_sort_id){
      return(
        <div className="has-text-centered">
          <button className={`button is-large ${this.props.fetching ? "is-loading" : ""}`} onClick={this.seenRequests}>確認</button>
          <button className={`button is-large ${this.props.fetching ? "is-loading" : ""}`} onClick={this.loadNext}>さらに読み込み</button>
        </div>
      )
    }
  }
  render(){
      return (
          <div>
            <Header page="/recent"/>
            <div className="hero is-bold is-info">
              <div className="hero-body">
                <div className="container">
                  <h1 className="title has-text-centered">最新の翻訳本</h1>
                </div>
              </div>
            </div>
            <section className="level"></section>
            <div className="container">
              {this.renderRecent()}
            </div>
            <section className="level"></section>
              {this.renderNext()}
            <section className="level"></section>
          <Footer/>
        </div>
      );
  }
}


const mapStateToProps = (state) => {
  return {
    recent_book_relations: state.recenting.recent_book_relations,
    fetching: state.recenting.fetching,
    last_sort_id: state.recenting.last_sort_id,
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    recentBooks: (sort_id, num) => dispatch(RecentActions.recentRequest(sort_id, num, true)),
    seenBooks: (sort_id) => dispatch(RecentActions.seenRequest(sort_id))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(BookManageView)