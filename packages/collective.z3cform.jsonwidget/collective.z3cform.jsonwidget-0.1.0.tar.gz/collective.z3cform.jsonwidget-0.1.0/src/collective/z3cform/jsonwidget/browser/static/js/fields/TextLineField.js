import React from 'react';
import PropTypes from 'prop-types';

// import './index.less';

const TextLineField = ({ value }) => {
  return (
    <input
      type="text"
      value={value}
      onChange={() => {
        console.log('cambiato');
      }}
    />
  );
};
TextLineField.propTypes = {
  value: PropTypes.string,
};

export default TextLineField;
