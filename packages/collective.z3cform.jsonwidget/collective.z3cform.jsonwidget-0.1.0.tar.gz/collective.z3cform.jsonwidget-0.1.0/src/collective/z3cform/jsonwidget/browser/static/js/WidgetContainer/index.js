import React, { Component } from 'react';
import PropTypes from 'prop-types';
import WidgetDataContainer from '../WidgetDataContainer';
import axios from 'axios';
import WidgetContext from '../utils/widgetContext';
import { getTranslationCatalog } from '../utils/i18n';
import arrayMove from 'array-move';

class WidgetContainer extends Component {
  constructor(props) {
    super(props);
    const fieldValue = document.getElementById(props.fieldId).value;
    const value = fieldValue.length > 0 ? JSON.parse(fieldValue) : [];

    this.getTranslationFor = msgid => {
      const { translations } = this.state;
      return translations[msgid] || msgid;
    };

    const updateWidgetField = value => {
      document.getElementById(this.props.fieldId).value = JSON.stringify(value);
    };

    this.addRow = () => {
      let newValue = this.state.value.map(entry => entry);
      let emptyRow = {};
      const { schema } = this.props;
      schema.fieldsets[0].fields.forEach(fieldId => {
        const field = schema.fields[fieldId];
        if (field.type === 'string') {
          emptyRow[fieldId] = '';
        } else {
          emptyRow[fieldId] = [];
        }
      });
      newValue.push(emptyRow);
      this.setState({
        ...this.state,
        value: newValue,
      });
      updateWidgetField(newValue);
    };

    this.removeRow = row => {
      let newValue = this.state.value.filter((entry, idx) => idx !== row);
      this.setState({
        ...this.state,
        value: newValue,
      });
      updateWidgetField(newValue);
    };

    this.moveRow = ({ from, to }) => {
      const newValue = arrayMove(this.state.value, from, to);
      this.setState({
        ...this.state,
        value: newValue,
      });
      updateWidgetField(newValue);
    };
    this.updateField = ({ id, value, row }) => {
      let updatedValue = this.state.value;
      updatedValue[row][id] = value;
      this.setState({
        ...this.state,
        value: updatedValue,
      });
      updateWidgetField(updatedValue);
    };
    this.state = {
      value,
      vocabularies: {},
      translations: {},
      addRow: this.addRow,
      removeRow: this.removeRow,
      moveRow: this.moveRow,
      updateField: this.updateField,
      getTranslationFor: this.getTranslationFor,
    };
    // fetch translations
    getTranslationCatalog().then(data => {
      this.setState({ ...this.state, translations: data });
    });
    // fetch vocabularies
    const { schema } = props;
    const fetches = [];
    schema.fieldsets[0].fields.forEach(fieldId => {
      const field = schema.fields[fieldId];
      if (field.vocabulary) {
        fetches.push({ id: fieldId, url: field.vocabulary['@id'] });
      }
      if (field.widgetOptions) {
        const { vocabulary } = field.widgetOptions;
        if (vocabulary) {
          fetches.push({ id: fieldId, url: vocabulary['@id'] });
        }
      }
      Promise.all(
        fetches.map(fetchItem =>
          axios({
            method: 'GET',
            url: fetchItem.url,
            headers: { Accept: 'application/json' },
          }).then(data => {
            this.setState({
              ...this.state,
              vocabularies: {
                ...this.state.vocabularies,
                [fetchItem.id]: data.data,
              },
            });
          }),
        ),
      );
    });
  }
  render() {
    return (
      <WidgetContext.Provider
        value={{ ...this.state, schema: this.props.schema }}
      >
        <WidgetDataContainer></WidgetDataContainer>
      </WidgetContext.Provider>
    );
  }
}
WidgetContainer.propTypes = {
  baseUrl: PropTypes.string,
  fieldId: PropTypes.string,
  schema: PropTypes.object,
};

export default WidgetContainer;
