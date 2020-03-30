import makeRequest from './helpers/makeRequest';

export function getDateData(date){
    return( 
        makeRequest(`${date.year}/${date.month}/${date.day}`)
    )
   
}

export function getMonthData(date){
    return ( 
        makeRequest(`${date.year}/${date.month}`)
    );
}

export function getHurals(date){
    return ( 
        makeRequest(`hurals`)
    );
}

export function getRituals(date){
    return ( 
        makeRequest(`rituals`)
    );
}

