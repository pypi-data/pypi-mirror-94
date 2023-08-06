import React from 'react';

const WidgetContext = React.createContext({
  schema: {},
  vocabularies: {},
  value: [],
  addRow: () => {},
  deleteRow: () => {},
  moveRow: () => {},
  updateField: () => {},
  getTranslationFor: () => {},
});

export default WidgetContext;
