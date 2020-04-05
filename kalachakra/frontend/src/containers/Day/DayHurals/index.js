import React from 'react';
import PropTypes from 'prop-types';
import HuralSelect from '~/components/huralSelect';


export default function DayHurals(props) {

    const changeMorningHutal = (event) => {
        props.changeDay({ morning_hural_id: +event.target.value })
    }

    const changeDayHutal = (event) => {
        props.changeDay({ day_hural_id: +event.target.value })
    }


    return (
        < >
            <span className="">
                Утренний хурал
                    </span>
            <span className="">
                <HuralSelect
                    hurals={props.hurals}
                    changeHural={changeMorningHutal}
                    selectedId={props.dataFields.morning_hural_id}
                    disabled={Boolean(props.blockedFields.indexOf('morning_hural_id') + 1)}
                />
            </span>
            <br />
            <span className="">
                Вечерний хурал
                    </span>
            <span className="">
                <HuralSelect
                    hurals={props.hurals}
                    changeHural={changeDayHutal}
                    selectedId={props.dataFields.day_hural_id}
                    disabled={Boolean(props.blockedFields.indexOf('day_hural_id') + 1)}
               />
            </span>

        </>
    );
}

DayHurals.propTypes = {
    hurals: PropTypes.array,
    blockedFields: PropTypes.array,
    changeDay: PropTypes.func
};

DayHurals.defaultProps = {
    hurals: [],
    blockedFields: [],
    changeDay: ()=>{}
};