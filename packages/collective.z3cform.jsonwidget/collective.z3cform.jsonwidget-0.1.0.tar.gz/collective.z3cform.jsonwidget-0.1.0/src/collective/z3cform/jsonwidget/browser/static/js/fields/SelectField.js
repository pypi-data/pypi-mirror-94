import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import WidgetContext from '../utils/widgetContext';

// import './index.less';

const SelectField = ({ value, id, row, multi }) => {
  const { vocabularies, updateField } = useContext(WidgetContext);
  const vocab = vocabularies[id];
  if (!vocab) {
    return '';
  }
  const options = vocab.items.map(item => {
    return { value: item.token, label: item.title };
  });
  return (
    <Select
      isMulti={multi ? true : false}
      isClearable={true}
      value={options.filter(option => {
        if (Array.isArray(value)) {
          return value.includes(option.value);
        } else {
          return value === option.value;
        }
      })}
      options={options}
      onChange={option => {
        let newValue = null;
        if (Array.isArray(value)) {
          newValue = option.map(item => item.value);
        } else {
          newValue = option.value;
        }
        updateField({ row, id, value: newValue });
      }}
    />
  );
};
SelectField.propTypes = {
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.array]),
  id: PropTypes.string,
  multi: PropTypes.bool,
  row: PropTypes.number,
};

export default SelectField;
