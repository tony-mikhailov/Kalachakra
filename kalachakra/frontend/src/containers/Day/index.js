import React, { useState, useEffect } from 'react';
import PropTypes, { func } from 'prop-types';
import { Container, Row, Button, Col } from 'react-bootstrap';
import getDateFromURL from '~/api/helpers/getDate';
import { getDateData, getHurals, getRituals} from  '~/api/getData.js';
import { postDateData, postDateDeleteEvent } from '~/api/postData';
import dayFlagsStore from '~/store/dayFlags.js';
import DayHead from './DayHead';
import DayMoon from './DayMoon';
import DayFlags from '~/containers/DayFlags';
import DayHurals from './DayHurals';
import DayEvents from './DayEvents';


export default function Day(props) {

    let dataFields = {}, 
        setDataFields;
    for (let i = 0, count = dayFlagsStore.length; i < count; i++){
        dataFields[dayFlagsStore[i].id] = null;
    }
    [dataFields, setDataFields] = useState(dataFields);

    const [blockedFields, setblockedFields] = useState([]);
    const [hurals, setHurals] = useState([]);
    const [rituals, setRituals] = useState([]);

    const date = getDateFromURL(props.match.params);

    const changeDay = (param)=>{

        setblockedFields([
            ...blockedFields,
            ...Object.keys(param)
        ]);

        return(
            postDateData(date, param)
            .then(function(data){
                setDataFields(data);
                setblockedFields(
                    blockedFields.filter(
                        item => { return (Object.keys(param).indexOf(item) + 1) }
                    )
                );
            })
        )
    }

    const changeMoonDay = (delta)=>{
        changeDay({ moon_day_no: dataFields.moon_day_no + delta })
    }

    const deleteEvent = (id) => {
        return (
            postDateDeleteEvent(date, { id })
        )
    }

    useEffect(() => {
        getDateData(date)
            .then(result=>{
                setDataFields(result);
            })
        
    }, [props.match.params]);

    useEffect(() => {

        getHurals(date)
            .then(result => {
                if (result.length > 0) {
                    setHurals(result);
                }
            });

        getRituals(date)
            .then(result => {
                if (result.length > 0) {
                    setRituals([
                        { id: 0, short_name:'Выберите ритуал'},
                        ...result
                    ]);
                }
            });
    }, []);

    return (
        <Container>
            <Row className="mt-3 d-flex align-items-center">
                <Col>
                    <DayHead date={date} />
                </Col>
            </Row>

            <Row className="mt-3 d-flex align-items-center">
                <Col>
                    <DayMoon
                        dataFields={dataFields}
                        isBlocked={blockedFields.indexOf('moon_day_no') + 1}
                        changeMoonDay={changeMoonDay}
                    />
                </Col>
            </Row>

            <Row className="mt-3 ">
                <Col lg={6} >
                    <DayFlags
                        dataFields={dataFields}
                    />
                </Col>
            </Row>

            <Row className="mt-3 ">
                <Col lg={6}>
                    <DayHurals
                        hurals={hurals}
                        dataFields={dataFields}
                        blockedFields={blockedFields}
                        changeDay={changeDay}
                    />
                </Col>
            </Row>

            <Row className="mt-3 mb-3 flex-column">
                <Col lg={6}>
                    <DayEvents 
                            rituals={rituals}
                            events={dataFields.events}
                            blockedFields={blockedFields}
                            changeDay={changeDay}
                            deleteEvent={deleteEvent}
                        />
                </Col>
            </Row>

        </Container>
    );
}

Day.propTypes = {
    list: PropTypes.array
};

Day.defaultProps = {
    list: []
};