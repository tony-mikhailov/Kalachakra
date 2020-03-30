import Month from '~/containers/Month';
import Day from '~/containers/Day';
import Page404 from '~/containers/error404';

let routes = [
    {
        name: 'home',
        url: '/',
        component: Month,
        exact: true
    },
    {
        name: 'today',
        url: '/today',
        component: Day,
        exact: true
    },
    {
        name: 'day',
        url: '/:year/:month/:day',
        component: Day,
        exact: true
    },
    {
        name: 'month',
        url: '/:year/:month',
        component: Month,
        exact: true
    },
    {
        url: '**',
        component: Page404
    }
];

let routesMap = {};

routes.forEach((route) => {
    if(route.hasOwnProperty('name')){
        routesMap[route.name] = route.url;
    }
});

let urlBuilder = function(name, params){
    if(!routesMap.hasOwnProperty(name)){
        return null;
    }

    let url = routesMap[name]; // news/:id

    for(let key in params){
        url = url.replace(':' + key, params[key]);
    }

    return url;
}

export default routes;
export {routesMap, urlBuilder};