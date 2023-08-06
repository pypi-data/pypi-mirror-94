define([
  'base/js/namespace',
  'base/js/events'
],
  function (Jupyter, events) {
    const injectParams = () => {
      getParams().forEach(function (value, key) {
        const cell = Jupyter.notebook.insert_cell_above('code')
        cell.set_text(`${key} = ${value};`);

        hideElement(cell.element[0]);
        executeCell(cell);
      });
    };

    const hideAndExecuteHiddenCells = () => {
      const cells = Jupyter.notebook.get_cells();
      let hiddenCells = cells.filter(cell => cell.get_text().startsWith('#hideCell'));

      hiddenCells.forEach(cell => {
        hideElement(cell.element[0])
        executeCell(cell, 2000)
      });
    };

    const hideAndExecuteInputCells = () => {
      const cells = Jupyter.notebook.get_cells();
      let hiddenCells = cells.filter(cell => cell.get_text().startsWith('#hideInput'));

      hiddenCells.forEach(cell => {
        hideElement(cell.element[0].querySelector('.input'))
        executeCell(cell, 2000)
      });
    };


    const injectSubmitButton = () => {
      const cell = Jupyter.notebook.insert_cell_at_bottom('code');
      cell.set_text(submitButton);

      hideElement(cell.element[0].querySelector('.input'));
      executeCell(cell, 5000)
    }

    const initialize = () => {
      injectParams();
      injectSubmitButton();
      hideAndExecuteHiddenCells();
      hideAndExecuteInputCells();
    }

    function load_ipython_extension() {
      events.on("kernel_ready.Kernel", function () {
        if (Jupyter.notebook !== undefined && Jupyter.notebook._fully_loaded) {
          initialize()
        } else {
          events.on("notebook_loaded.Notebook", function () {
            initialize()
          })
        }
      });
    }

    return {
      load_ipython_extension: load_ipython_extension
    };
  }
);

const hideElement = (element) => {
  element.style.position = "absolute";
  element.style.clip = "rect(1px, 1px, 1px, 1px)"
  element.style.overflow = "hidden"
  element.style.width = "1px";
  element.style.height = "1px";
}

const getParams = () => {
  return new URL(window.location.href).searchParams;
}

const executeCell = (cell, timeout = 1000) => {
  window.setTimeout(function () {
    cell.execute()
  }, timeout);
}

const submitButton = `from ipywidgets import widgets, Button, HBox, Output, VBox, Layout
import requests
btn = widgets.Button(description='Ergebnis absenden')

try:
    if not endpoint or not uuid or not username or not lm:
        raise RuntimeError("Parameters missing");
except RuntimeError as e:
    print(e)

score = lm.get_score;
display(btn);

def submit_score(obj):
    try:
        response = requests.post(endpoint, data= {"uuid": uuid, "score": score, "username": username})
        if response.status_code != 200:
            raise RuntimeError("Fehler beim Request: " + str(response.status_code))
    except Exception as e:
        print(e)
    else:
        print("Durchführung erfolgreich abgegeben!")
btn.on_click(submit_score)`;
