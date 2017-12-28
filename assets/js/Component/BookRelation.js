/**
 * Created by kasajei on 2017/05/12.
 */
import React from 'react';

export default class BookRelation extends React.Component{
  render(){
    if (this.props.amazon && this.props.amazon.title) {
      const style = {
        minWidth: 360
      };
      return (
        <div className="column">
              <div className="box media" style={style}>
               <figure className="media-left">
                  <p className="image">
                    <a href={this.props.amazon.offer_url} target="_blank">
                     <img src={this.props.amazon.medium_image_url}/>
                    </a>
                  </p>
               </figure>
               <div className="media-content">
                  <div className="content">
                    <p><a href={this.props.amazon.offer_url} target="_blank"><strong>{this.props.amazon.title} </strong></a><br/>
                       <small>著者：{this.props.amazon.author}（{this.props.original?this.props.original.author:this.props.amazon.author}）</small><br/>
                       <small>原著：<a href={this.props.original?this.props.original.offer_url:"#"}　target="_blank"><strong>{this.props.original? this.props.original.title:"見つかりませんでした"}</strong> </a></small>
                     </p>
                  </div>

               </div>
              </div>
        </div>
      );
    }else{
      return (
        <div className="column">
        <a>
                <article className="box media">
                 <figure className="media-left">
                    <p className="image">
                       <img src="https://placeholdit.imgix.net/~text?txtsize=12&txt=NoImage&w=111&h=160"/>
                    </p>
                 </figure>
                 <div className="media-content">
                    <div className="content">
                       <p><strong>見つかりませんでした。</strong><br/>
                         <small>見つかりませんでした</small>
                       </p>
                    </div>
                 </div>
                </article>
        </a>
        </div>
      );
    }
  }
}

