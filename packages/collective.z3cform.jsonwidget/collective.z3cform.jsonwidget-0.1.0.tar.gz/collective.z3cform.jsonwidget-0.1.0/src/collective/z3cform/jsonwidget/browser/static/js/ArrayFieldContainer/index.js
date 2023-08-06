import React from 'react';
import SelectField from '../fields/SelectField';
import ReferenceField from '../fields/ReferenceField';

// import './index.less';

const ArrayFieldContainer = props => {
  const { type } = props.items;
  if (type === 'string') {
    return <SelectField {...props} multi={true}></SelectField>;
  } else if (type === 'relation') {
    return <ReferenceField {...props}></ReferenceField>;
  }
};
ArrayFieldContainer.propTypes = {};

export default ArrayFieldContainer;
