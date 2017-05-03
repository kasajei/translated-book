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


class MainView extends React.Component{
  componentDidMount() {
    this.props.searchBooks(null, "THE HAPPINESS TRACK", null);
  }
  renderBooks(){
    return (
      this.props.books.map(function (book) {
        return <Book book={book} key={book.title}/>
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
        </div>
      </div>
    );
  }
}


const mapStateToProps = (state) => {
  return {
    books: state.booking.books
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    searchBooks: (isbn, title, author) => dispatch(BooksActions.searchRequest(isbn, title, author))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(MainView)