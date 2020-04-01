import makeRequest from './helpers/makeRequest';

export function postDateData(date, params) {
    return (
        makeRequest(`${date.year}/${date.month}/${date.day}`, {
            method: 'POST',
            redirect: "follow",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
    )

}

export function postDateDeleteEvent(date, params) {
    return (
        makeRequest(`${date.year}/${date.month}/${date.day}/delete_event`, {
            method: 'POST',
            redirect: "follow",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
    )

}

export function postMonthData(date, params) {
    return (
        makeRequest(`${date.year}/${date.month}`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        })
    );
}
