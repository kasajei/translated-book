/**
 * Created by kasajei on 2017/04/03.
 */

import apisauce from 'apisauce'

const host = window.location.host.split(':')[0];
const ROOT_URL = (process.env.NODE_ENV == "production" ? 'https://' + host : 'http://' + host+':8000') + '/api/v1';

const create = (baseURL = ROOT_URL) => {
  const api = apisauce.create({
    baseURL,
    timeout: 10000
  });

  const search = (isbn, title, author) => api.get('/search/', {
    "isbn": isbn,
    "title": title,
    "author": author,
  });

  const amazon = (title, original_title) => api.get('/amazon/', {
    "title": title,
    "original_title": original_title,
  });

  return {
    // a list of the API functions from step 2
    search,
    amazon,
  }
};

// let's return back our create method as the default.
export default {
  create
}
