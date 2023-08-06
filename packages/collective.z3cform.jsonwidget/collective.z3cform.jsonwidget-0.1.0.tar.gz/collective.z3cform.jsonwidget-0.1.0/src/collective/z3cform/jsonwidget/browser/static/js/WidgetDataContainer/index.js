import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import EntryColumnContainer from '../EntryColumnContainer';
import WidgetContext from '../utils/widgetContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faPlus,
  faTrash,
  faArrowUp,
  faArrowDown,
} from '@fortawesome/free-solid-svg-icons';

import './index.less';

const WidgetDataContainer = () => {
  const {
    value,
    schema,
    addRow,
    removeRow,
    moveRow,
    getTranslationFor,
  } = useContext(WidgetContext);

  return (
    <div className="data-wrapper">
      {value.map((entry, idx) => (
        <div className="json-row" key={idx}>
          <div className="row-header">
            {idx + 1 !== value.length && (
              <button
                className="standalone"
                type="button"
                onClick={e => {
                  e.preventDefault();
                  moveRow({ from: idx, to: idx + 1 });
                }}
              >
                <FontAwesomeIcon icon={faArrowDown} />
              </button>
            )}
            {idx > 0 && (
              <button
                className="standalone"
                type="button"
                onClick={e => {
                  e.preventDefault();
                  moveRow({ from: idx, to: idx - 1 });
                }}
              >
                <FontAwesomeIcon icon={faArrowUp} />
              </button>
            )}
            <strong>
              {getTranslationFor('Group')} {idx + 1}
            </strong>
            <button
              className="destructive"
              type="button"
              onClick={e => {
                e.preventDefault();
                removeRow(idx);
              }}
            >
              <FontAwesomeIcon icon={faTrash} />
            </button>
          </div>
          {schema.fieldsets[0].fields.map(fieldId => (
            <EntryColumnContainer
              key={`${idx}-${fieldId}`}
              value={entry[fieldId]}
              id={fieldId}
              row={idx}
            ></EntryColumnContainer>
          ))}
        </div>
      ))}
      <div className="data-footer">
        <button
          className="context"
          type="button"
          onClick={e => {
            e.preventDefault();
            addRow();
          }}
        >
          <FontAwesomeIcon icon={faPlus} /> {getTranslationFor('Add')}
        </button>
      </div>
    </div>
  );
};
WidgetDataContainer.propTypes = {
  value: PropTypes.array,
  schema: PropTypes.object,
  vocabularies: PropTypes.object,
};

export default WidgetDataContainer;
