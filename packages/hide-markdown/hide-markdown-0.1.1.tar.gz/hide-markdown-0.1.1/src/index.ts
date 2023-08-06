import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IDisposable, DisposableDelegate } from '@lumino/disposable';

import { PanelLayout } from '@lumino/widgets';

import { ToolbarButton } from '@jupyterlab/apputils';

import { DocumentRegistry } from '@jupyterlab/docregistry';

import {
  NotebookPanel,
  INotebookModel
} from '@jupyterlab/notebook';

import '../style/index.css';

/**
 * Initialization data for the hide-markdown extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'hide-markdown:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
    console.log('JupyterLab extension hide-markdown is activated!');
  }
};

export class ButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    const hideMD = () => {
      panel.content.widgets.forEach(cell => {
        if (cell.model.type === 'markdown') {
          const layout = cell.layout as PanelLayout;
          layout.widgets[1].hide();
        }
      });
      hideButton.hide();
      showButton.show();
    };
    const showMD = () => {
      panel.content.widgets.forEach(cell => {
        if (cell.model.type === 'markdown') {
          const layout = cell.layout as PanelLayout;
          layout.widgets[1].show();
        }
      });

      hideButton.show();
      showButton.hide();
    };

    const hideButton = new ToolbarButton({
      className: 'hmButton',
      iconClass: 'fas fa-file-code  hm-buttons',
      onClick: hideMD,
      tooltip: 'Hide Markdown'
    });

    const showButton = new ToolbarButton({
      className: 'hmButton',
      iconClass: 'fas fa-file-contra hm-buttons',
      onClick: showMD,
      tooltip: 'Show Markdown'
    });

    showButton.hide();

    panel.toolbar.insertItem(11, 'hideInput', hideButton);
    panel.toolbar.insertItem(11, 'showInput', showButton);

    return new DisposableDelegate(() => {
      hideButton.dispose();
      showButton.dispose();
    });
  }
}

export default extension;
