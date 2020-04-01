import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';


export default function DayHead(props) {

    return (
        <>
            <Link
                to={`/${props.date.dayPrev.year}/${props.date.dayPrev.month}/${props.date.dayPrev.day}`}
                className='btn btn-primary ml-3 mr-1'
            >
                {'<'}
            </Link>

            {props.date.day} 
            <u>
                <Link to={`/${props.date.year}/${props.date.month}`} className='ml-1'>{props.date.monthWord} {props.date.year} </Link>
            </u>
            
            <Link
                to={`/${props.date.dayNext.year}/${props.date.dayNext.month}/${props.date.dayNext.day}`}
                className='btn btn-primary ml-1'
            >
                {'>'}
            </Link>
        </>

    );
}

DayHead.propTypes = {
    date: PropTypes.object
};

DayHead.defaultProps = {
    date: {}
};