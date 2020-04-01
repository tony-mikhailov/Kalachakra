import React, { useState, useEffect } from 'react';
import { Container, Button, Row, Col } from 'react-bootstrap';
import getDateFromURL from '~/api/helpers/getDate';
import { getMonthData, getHurals } from '~/api/getData.js'
import { postDateData } from '~/api/postData.js'
import { Link } from 'react-router-dom';
import style from './month.module.css';
import MonthLine from './MonthLine/index';

export default function Month(props) {

    const date = getDateFromURL(props.match.params);

    const [list, setlist] = useState([]);
    const [hurals, setHurals] = useState([]);

    const postChangedDay=(day, param)=>{
        const postDate = {
            ...date,
            day
        }
        return postDateData(postDate, param)
    }

    const changeHural = (year, day, hural, id)=>{
        postChangedDay(day, { [hural]: id})
            .then(result => {
                changeDay(day, result)
            })
    }

    const changeDay = (day, params) => {
        const newlist = list.map(item => {
            if (item.day == day) {
                const newItem = {
                    ...item,
                    ...params
                }
                return newItem;
            }
            return item;
        });
        setlist(newlist);
    }


    useEffect(() => {

        getMonthData(date)
            .then(result => {
                if (result.length > 0) {
                    setlist(result);
                }
            })
    }, [props.match.params]);

    useEffect(() => {

        getHurals(date)
            .then(result => {
                if (result.length > 0) {
                   setHurals(result);
                }
            })
    }, []);

    return (
        <Container>
            <Row className="mt-3 ml-3 d-flex align-items-center">
                <Link to={`/${date.monthPrev.year}/${date.monthPrev.month}`} className='mr-1 btn btn-primary'>{'<'}</Link>
                <span className={style.month_title}>
                    {date.monthWord} {date.year} 
                </span>
                <Link to={`/${date.monthNext.year}/${date.monthNext.month}`} className='ml-1 btn btn-primary'>{'>'}</Link>
           </Row>
           <Row className='mt-3'>
               <Col>
                    {<MonthLine
                        date={date}
                        lines={list}
                        hurals={hurals}
                        changeHural={changeHural}
                    />}   
               </Col>
           </Row>
        </Container>
    );
}
