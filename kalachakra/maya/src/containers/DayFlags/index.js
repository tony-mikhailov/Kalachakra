import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import style from './day.module.css';
import dayFlagsStore from '~/store/dayFlags.js';
import { postDateData } from '~/api/postData';
import { Tooltip, OverlayTrigger} from 'react-bootstrap';

export default function DayFlags(props) {

    const [dataFields, setDataFields] = useState(props.dataFields);
    const [blockedFields, setblockedFields] = useState([]);

    const changeDay = (param) => {

        const newArr = [
            ...blockedFields,
            ...Object.keys(param)
        ]
        setblockedFields(newArr);

        return (
            postDateData(props.dataFields, param)
                .then(function (data) {
                    setDataFields(data);
                    setblockedFields(
                        blockedFields.filter(
                            item => { return (Object.keys(param).indexOf(item) + 1) }
                        )
                    );
                })
        )
    }

    useEffect(() => {
        setDataFields(props.dataFields)
    }, [props.dataFields]);

    return (
        <>
            {
                dayFlagsStore.map((flag) => {
                    const isBlocked = Boolean(blockedFields.indexOf(flag.id) + 1);
                    return (
                        <OverlayTrigger
                            key={flag.id}
                            placement="top"
                            delay={{ show: 150, hide: 150 }}
                            overlay={<Tooltip >
                                        {flag.title}
                                    </Tooltip>}
                        >
                            <span
                                className={"mr-3 " + 
                                            style.day_attr + ' ' + 
                                            (dataFields[flag.id] ? '' : style.day_param_off) + ' ' + 
                                            (isBlocked ? style.day_param_blocked : '')
                                        }
                                onClick={() => { 
                                    if (isBlocked) return;
                                    changeDay({ [flag.id]: !dataFields[flag.id] });
                                }}
                            >
                                {flag.flag}  {' '}
                            </span>
                        </OverlayTrigger>
                        )
                })
            }
        </>

    );
}

DayFlags.propTypes = {
    dataFields: PropTypes.object
};

DayFlags.defaultProps = {
    dataFields: {}
};