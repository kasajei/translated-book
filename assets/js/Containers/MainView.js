import React from 'react';
import { Link } from 'react-router';
import BooksActions from '../Redux/BooksRedux'
import RecentActions from '../Redux/RecentRedux'
import { connect } from 'react-redux'
import Footer from '../Component/Footer'
import Header from '../Component/Header'
import Amazon from '../Component/Amazon'

class Book extends React.Component{
  constructor(props){
    super(props);
    this.select_book = this.select_book.bind(this);
  }
  select_book(){
    this.props.selectBook(this.props.book);
  }
  render(){
    return (
      <a className={`panel-block ${this.props.is_active ? "is-active" : ""}`} onClick={this.select_book}>
        <li className="book">
          <i className="fa fa-user"></i> <small>{this.props.book.author}</small>
          <ul>
            <li><span className="list-icon"><i className="fa fa-book"></i></span> <small>{this.props.book.original_title}</small></li>
            <li><span className="list-icon"><i className="fa fa-book"></i></span> <small>{this.props.book.title}</small> </li>
          </ul>
        </li>
      </a>
    );
  }
}


class MainView extends React.Component{
  constructor(prop){
    super(prop);
    this.state = {
      search_option: "title",
      search_text: null,
      search:{},
      is_search: false,
      error: null,
    };
    this.selectSearchOption = this.selectSearchOption.bind(this);
    this.changeText = this.changeText.bind(this);
    this.search = this.search.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.renderBooks = this.renderBooks.bind(this);
  }
  componentWillMount(){
    if (this.props.recent_book_relations.length === 0) {
      this.props.recentBooks(null, 20)
    }
  }
  componentWillReceiveProps(newProps){
    if (newProps.books != this.props.books && newProps.books.length > 0){
      this.props.selectBook(newProps.books[0])
    }
    if (newProps.selected_book != this.props.selected_book){
      const {title, original_title} = newProps.selected_book;
      this.props.amazonBooks(title, original_title);
    }

    if (newProps.books.length == 0 && this.props.fetching){
      this.setState({error:"見つかりませんでした"});
    }
  }
  selectSearchOption(e){
    const {search_text} = this.state;
    const search = {};
    search[e.target.value] = search_text;
    this.setState({search_option:e.target.value, search:search})
  }
  changeText(e){
    const { search_option } = this.state;
    const search = {};
    search[search_option] = e.target.value;
    this.setState({search:search, search_text:e.target.value})
  }
  handleKeyPress(e){
    if(e.key === "Enter"){
      this.search()
    }
  }
  search(){
    const {search} = this.state;
    this.props.searchBooks(search["isbn"] ||null, search["title"] || null, search["author"] || null);
    this.setState({error:null});
  }
  renderBooks(){
    const selectBook = this.props.selectBook;
    var is_active = false;
    const selected_book = this.props.selected_book;
    return (
      this.props.books.map(function (book) {
        if (selected_book){
          is_active = (selected_book.isbn == book.isbn)
        }
        return <Book book={book} selectBook={selectBook} is_active={is_active} key={book.isbn}/>
      })
    )
  }
  renderMenu(){
    if(this.props.books.length >0) {
      return (
        <div className="submenu column is-3">
          <aside className="box menu">
           <p className="menu-label">
              翻訳本候補一覧
           </p>
           <ul className="menu-list">
                {this.renderBooks()}
            </ul>
          </aside>
        </div>
      );
    }
  }
  renderAmazon() {
    return (
      <div className="columns">
        <Amazon amazon={this.props.original_book}/>
        <Amazon amazon={this.props.translated_book}/>
      </div>
    )
  }
  renderOthers(){
    return(
      this.props.other_books.map(function (amazon) {
        return <Amazon amazon={amazon} key={amazon.asin}/>
      })
    )
  }
  renderRecent(){
    if (this.props.recent_book_relations.length > 0){
      return(
        <div className="container is-fluid">
          <h2 className="subtitle is-bold"><Link to="/recent">新刊の翻訳本</Link></h2>
          <div className="columns" style={{overflow:"scroll"}}>
          {
            this.props.recent_book_relations.map(function (book_relation){
              return <Amazon amazon={book_relation.translated_book} key={book_relation.translated_book.asin}/>
            })
          }
          </div>
        </div>
      )
    }
  }
  renderMain(){
    if (this.props.books.length > 0 && !this.props.fetching){
      return(
        <div className="column">
          <h2 className="subtitle is-bold">翻訳本</h2>
          {this.renderAmazon()}
          <hr/>
          <h2 className="subtitle is-bold">関連書</h2>
          <div className="container">
              {this.renderOthers()}
          </div>
        </div>
      )
    }else if(this.props.fetching) {
      return (
        <div className="column has-text-centered">
          <button className="button is-loading is-large is-expanded has-text-centered ">読み込んでいます</button>
        </div>
      )
    }else if(this.state.error){
      return(
        <div className="column">
          <article className="message is-warning">
            <div className="message-body">
              見つかりませんでした
            </div>
          </article>
        </div>
      )
    }else{
      return(
        <div className="column">
        </div>
      )
    }
  }
  render(){
    return (
      <div>
        <Header page="/"/>
        <div className="hero is-bold is-info is-medium">
          <div className="hero-body">
            <div className="container">
              <h1 className="title has-text-centered">翻訳本サーチα</h1>
              <h2 className="subtitle has-text-centered">探しづらい翻訳本を一発検索(したい)</h2>
                <div className="field has-addons column has-addons-centered">
                  <p className="control ">
                    <span className="select">
                      <select onChange={this.selectSearchOption}>
                        <option value="title">タイトル</option>
                        <option value="author">著者</option>
                        <option value="isbn">isbn</option>
                      </select>
                    </span>
                  </p>
                  <p className="control">
                  <input className="input is-primary" size="54" type="text" placeholder="で探す" onChange={this.changeText} onKeyPress={this.handleKeyPress}/>
                  </p>
                  <p className="control">
                  <button className={`button is-primary ${this.props.fetching ? "is-loading" : ""}`} onClick={this.search}>検索</button>
                  </p>
              </div>
            </div>
          </div>
        </div>
        <section className="level"></section>
        <div className="container is-fluid">
          <main className="columns">
            {this.renderMain()}
            {this.renderMenu()}
  　　　　　</main>
        </div>
        <section className="level"></section>
            {this.renderRecent()}
        <section className="level"></section>
          <Footer/>
        </div>
    );
  }
}


const mapStateToProps = (state) => {
  return {
    books: state.booking.books,
    selected_book: state.booking.selected_book,
    original_book: state.booking.original_book,
    translated_book: state.booking.translated_book,
    other_books: state.booking.other_books,
    fetching: state.booking.fetching,
    recent_book_relations: state.recenting.recent_book_relations,
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    searchBooks: (isbn, title, author) => dispatch(BooksActions.searchRequest(isbn, title, author)),
    amazonBooks: (title, original_title) => dispatch(BooksActions.amazonRequest(title, original_title)),
    selectBook: (book) => dispatch(BooksActions.selectBook(book)),
    recentBooks: (sort_id, num) => dispatch(RecentActions.recentRequest(sort_id, num))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(MainView)