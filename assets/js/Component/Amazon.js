/**
 * Created by kasajei on 2017/05/12.
 */
import React from 'react';

export default class Amazon extends React.Component{
  render(){
    if (this.props.amazon && this.props.amazon.title) {
      const style = {
        minWidth: 360
      };
      return (
        <div className="column">
        <a href={this.props.amazon.offer_url} target="_blank">
              <div className="box media" style={style}>
               <figure className="media-left">
                  <p className="image">
                     <img src={this.props.amazon.medium_image_url}/>
                  </p>
               </figure>
               <div className="media-content">
                  <div className="content">
                     <p><strong>{this.props.amazon.title} </strong><br/>
                       <small>{this.props.amazon.author}</small>
                     </p>
                  </div>
               </div>
              </div>
          </a>
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

