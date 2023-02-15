document.addEventListener('DOMContentLoaded', function() {
    load_table();
});

function load_table() {
    const file_id = document.querySelector('#filename').dataset.fileId
    const body = {"file_id": file_id, "headers": []}
    const selected_headers = document.querySelectorAll('.btn-group .active')
    selected_headers.forEach(header => {
        body['headers'].push(header.innerHTML)
    });
    fetch("/value_count_table/", {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
    .then((response) => response.json())
    .then((table) => {
        const buttons = table['buttons'];
        const btn_group = document.querySelector('.btn-group')
        console.log(btn_group.hasChildNodes())
        if (!btn_group.hasChildNodes()){
            buttons.forEach(button_value => {
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
                btn_group.append(button);
            });
        }
//        const rows = table['rows'];
    });
};
