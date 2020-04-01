import React from 'react';
import ReactDom from 'react-dom';
import App from './containers/App';

import 'bootstrap/dist/css/bootstrap.min.css';
import '../public/fonts/style.css'
import '~/style.css'

ReactDom.render(<App/>, document.querySelector('#app'));