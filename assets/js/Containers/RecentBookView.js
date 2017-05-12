import React from 'react';
import {Link} from 'react-router'
import BooksActions from '../Redux/BooksRedux'
import { connect } from 'react-redux'
import Footer from '../Component/Footer'
import Header from '../Component/Header'


class RecentBookView extends React.Component{
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
              <section className="level"></section>
            <Footer/>
          </div>
        );
    }
}


const mapStateToProps = (state) => {
  return {
    recent_book_relations: state.booking.recent_book_relations,
  }
};

const mapDispatchToProps = (dispatch) => {
  return {
    recentBooks: (sort_id, num) => dispatch(BooksActions.recentRequest(sort_id, num))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(RecentBookView)