/**
 * Created by kasajei on 2017/05/12.
 */
import React from 'react';
import { Link } from 'react-router';


export default class Header extends React.Component{
  renderMenu(){
    const menus = [
      {
        to: "/",
        title: "検索"
      },{
        to: "/recent",
        title: "最新"
      },
    ];
    const page = this.props.page;
    return (
      menus.map(function(menu){
        if (menu.to === page){
          return <Link to={menu.to} className="nav-item is-active is-tab" key={menu.to}>{menu.title}</Link>
        }else{
          return <Link to={menu.to} className="nav-item is-tab" key={menu.to}>{menu.title}</Link>
        }
      })
    )
  }
  render(){
    return(
      <header className="nav has-shadow">
          <div className="nav-left">
              <span className="nav-item">
               <span className="fa fa-book"></span>　<Link to="/">翻訳本サーチα</Link>
              </span>
          </div>
          <div className="nav-right">
            {this.renderMenu()}
          </div>
        </header>
    )
  }
}
