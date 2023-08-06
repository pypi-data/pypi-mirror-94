import React from 'react';
import PropTypes from 'prop-types';

// import './index.less';

const TextAreaField = ({ value }) => {
  return (
    <textarea
      value={value}
      onChange={() => {
        console.log('cambiato');
      }}
    ></textarea>
  );
};
TextAreaField.propTypes = {
  value: PropTypes.array,
};

export default TextAreaField;
