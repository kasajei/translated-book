/**
 * Created by kasajei on 2017/05/12.
 */
import React from 'react';

export default class Footer extends React.Component{
  render(){
    return(
      <footer className="footer">
        <div className="container">
          <div className="content has-text-centered">
            <p>
              <strong>翻訳本サーチ</strong> by <a href="http://twitter.com/kasajei">@kasajei</a>
            </p>
            <p>
              <a className="icon" href="https://github.com/kasajei/translated-book">
                <i className="fa fa-github"></i>
              </a>
            </p>
          </div>
        </div>
      </footer>
    )
  }
}
