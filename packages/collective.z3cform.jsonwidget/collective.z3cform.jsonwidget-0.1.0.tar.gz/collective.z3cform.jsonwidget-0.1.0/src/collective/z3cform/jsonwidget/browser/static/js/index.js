import React from 'react';
import ReactDOM from 'react-dom';
import WidgetContainer from './WidgetContainer';

document.addEventListener('DOMContentLoaded', function() {
  const widgets = document.getElementsByClassName('json-textarea-widget');
  const baseUrl = document.body.getAttribute('data-base-url');

  if (widgets.length) {
    Array.from(widgets).forEach(element => {
      const root = element.querySelector('.widget-wrapper');
      const schema = element.getAttribute('data-schema');
      const field = element.querySelector('.widget-field');
      ReactDOM.render(
        <WidgetContainer
          baseUrl={baseUrl}
          schema={JSON.parse(schema)}
          fieldId={field.getAttribute('id')}
        />,
        root,
      );
    });
  }
});
