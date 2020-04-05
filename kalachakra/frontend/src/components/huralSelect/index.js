import React from 'react';
import PropTypes from 'prop-types';


export default function HuralSelect(props) {

    const changeHural = (event) => {

        props.changeHural(event)
    }

    return (
        <select 
            className="form-control"
            value={props.selectedId} 
            onChange={changeHural}
            disabled={props.disabled}
        >
            {
                props.hurals.map(item=>{return(
                    <option 
                        key={item.id}
                        value={item.id}
                    >
                        {item.short_name}
                    </option>
                )})
            }
        </select>
    );
}

HuralSelect.propTypes = {
    hurals: PropTypes.array,
    changeHural: PropTypes.func,
    selectedId: PropTypes.number,
    disabled: PropTypes.bool
};

HuralSelect.defaultProps = {
    hurals: [],
    changeHural: PropTypes.func,
    selectedId: 0,
    disabled:false
};