import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';


export default function DayMoon(props) {

    return (
        <>
            Лунный день:
            <Button 
                variant="primary" 
                className="ml-1 mr-1 " 
                onClick={() => { props.changeMoonDay(-1) }}
                disabled={props.isBlocked}
            > - </Button>

            {props.dataFields.moon_day_no}

            <Button 
                variant="primary" 
                className="ml-1 mr-2" 
                onClick={() => { props.changeMoonDay(1) }}
                disabled={props.isBlocked}
            > + </Button>
        </>
    );
}

DayMoon.propTypes = {
    dataFields: PropTypes.object
};

DayMoon.defaultProps = {
    dataFields: {}
};