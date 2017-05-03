import React from 'react';
import {Link} from 'react-router'


export default class PostView extends React.Component{
    render(){
        return (
            <div>
                <header>
                    <h1>記事表示</h1>
                    <Link to="/">ホームへ</Link>
                </header>
                <div id="content">
                </div>
            </div>
        );
    }
}