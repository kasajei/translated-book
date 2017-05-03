import React from 'react';
import { Link } from 'react-router';
import BooksActions from '../Redux/BooksRedux'
import { connect } from 'react-redux'

class Book extends React.Component{
  render(){
    return (
      <div className="book">
        {this.props.book.author} : {this.props.book.title} / {this.props.book.original_title}
      </div>
    );
  }
}

class Amazon extends React.Component{
  render(){
    if (this.props.amazon) {
      return (
        <div className="amazon">
          <a href={this.props.amazon.offer_url}>{this.props.amazon.title} </a>
        </div>
      );
    }else{
      return (
        <div className="amazon">
        </div>
      );
    }
  }
}


class MainView extends React.Component{
  componentDidMount() {
    this.props.searchBooks(null, "イノベーションのジレンマ", null);
  }
  renderBooks(){
    return (
      this.props.books.map(function (book) {
        return <Book book={book} key={book.title}/>
      })
    )
  }
  renderAmazon(){
    return(
      <div>
        <Amazon amazon={this.props.original_book}/>
        <Amazon amazon={this.props.translated_book}/>
      </div>
    )
  }
  renderOthers(){
    return(
      this.props.other_books.map(function (amazon) {
        return <Amazon amazon={amazon} key={amazon.id}/>
      })
    )
  }
  render(){
    return (
      <div>
        <header>
          <h1>翻訳本サーチ</h1>
        </header>
        <div id="content">
          {this.renderBooks()}
          {this.renderAmazon()}
          <hr/>
          {this.renderOthers()}
        </div>
      </div>
    );
  }
}


const mapStateToProps = (state) => {
  return {
    books: state.booking.books,
    original_book: state.booking.original_book,
    translated_book: state.booking.translated_book,
    other_books: state.booking.other_books,
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    searchBooks: (isbn, title, author) => dispatch(BooksActions.searchRequest(isbn, title, author)),
    amazonBooks: (title, original_title) => dispatch(BooksActions.amazonRequest(title, original_title))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(MainView)