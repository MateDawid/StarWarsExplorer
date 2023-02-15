document.addEventListener('DOMContentLoaded', function() {
    load_table();
});

function prepare_body() {
    let body = {'headers': []}
    const file_id = document.querySelector('#filename').dataset.fileId
    body['file_id'] = file_id
    const selected_headers = document.querySelectorAll('.btn-group .active')
    selected_headers.forEach(header => {
        body['headers'].push(header.innerHTML)
    });
    return JSON.stringify(body)
}

function createHeaderButton(button_value) {
    let button = document.createElement('button');
    button.type = 'button';
    button.innerHTML = button_value;
    button.classList.add('btn', 'btn-light')
    button.addEventListener('click', function() {
        if (button.classList.contains('active')) {
            button.classList.remove('active');
        }
        else {
            button.classList.add('active');
        }
        load_table();
    });
    return button
}

function createTable(rows) {
    const tbody = document.querySelector('table tbody')
    tbody.innerHTML = ''
    const thead = document.querySelector('table thead')
    thead.innerHTML = ''
    rows.forEach((row,index) => {
        tr = document.createElement('tr');
        row.forEach(value => {
            let td = document.createElement('td')
            td.innerHTML = value
            tr.append(td)
        })
        if (index == 0) {
            tr.className = 'table-dark';
            thead.append(tr);
        }
        else {
            tr.className = 'table-secondary';
            tbody.append(tr)
        }
    });
}

function load_table() {

    const body = prepare_body()
    fetch("/value_count_table/", {
      method: "POST",
      body: body,
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
    .then((response) => response.json())
    .then((table) => {
        // Creating headers buttons if they don't already exist
        const btn_group = document.querySelector('.btn-group')
        if (!btn_group.hasChildNodes()){
            const buttons = table['buttons'];
            buttons.forEach(button_value => {
                let button = createHeaderButton(button_value);
                btn_group.append(button);
            });
        }
        // Displaying rows
        const rows = table['rows'];
        createTable(rows);
    });
};
