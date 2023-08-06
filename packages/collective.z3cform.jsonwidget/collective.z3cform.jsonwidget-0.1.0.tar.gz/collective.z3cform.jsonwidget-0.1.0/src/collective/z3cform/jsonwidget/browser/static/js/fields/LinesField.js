import React, { useContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faTrash } from '@fortawesome/free-solid-svg-icons';
import WidgetContext from '../utils/widgetContext';

import './LinesField.less';

const LineField = ({ value, row, updateField }) => {
  const [data, setData] = useState({ text: '', timeout: 0 });

  const updateText = targetValue => {
    if (data.timeout) {
      clearInterval(data.timeout);
    }
    const timeout = setTimeout(() => {
      updateField({ newValue: targetValue, row });
    }, 1000);
    setData({ text: targetValue, timeout });
  };
  useEffect(() => {
    setData({ text: value, timeout: 0 });
  }, [value]);

  return (
    <input
      type="text"
      className="input-line"
      value={data.text}
      onChange={e => updateText(e.target.value)}
    />
  );
};

const LinesField = ({ value, id, row }) => {
  const { updateField, getTranslationFor } = useContext(WidgetContext);
  const onUpdateRow = data => {
    const newValue = value.map((rowText, rowIdx) => {
      if (rowIdx === data.row) {
        return data.newValue;
      } else {
        return rowText;
      }
    });
    updateField({ row, id, value: newValue });
  };

  const onAddRow = e => {
    e.preventDefault();
    let newValue = value.map(text => text);
    newValue.push('');
    updateField({ row, id, value: newValue });
  };
  const onDeleteRow = deletedRow => {
    let newValue = value.filter((text, idx) => idx !== deletedRow);
    updateField({ row, id, value: newValue });
  };

  return (
    <div className="array-rows">
      {value.map((rowValue, idx) => (
        <div className="row" key={`${id}-row-${idx}`}>
          <div className="column">
            <LineField
              row={idx}
              updateField={onUpdateRow}
              value={rowValue}
            ></LineField>
          </div>
          <div className="column">
            <button
              className="destructive"
              type="button"
              onClick={e => {
                e.preventDefault();
                onDeleteRow(idx);
              }}
            >
              <FontAwesomeIcon icon={faTrash} />
            </button>
          </div>
        </div>
      ))}
      <button className="context" type="button" onClick={onAddRow}>
        <FontAwesomeIcon icon={faPlus} /> {getTranslationFor('Add')}
      </button>
    </div>
  );
};

LineField.propTypes = {
  value: PropTypes.string,
  row: PropTypes.number,
  updateField: PropTypes.func,
};
LinesField.propTypes = {
  value: PropTypes.array,
  id: PropTypes.string,
  row: PropTypes.number,
};

export default LinesField;
