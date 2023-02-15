let counter = 0;
const quantity = 10;

document.addEventListener('DOMContentLoaded', function() {
    load();
    document.querySelector('#load').onclick = load;
});

function load() {
    const start = counter;
    let end = start + quantity - 1;
    // Add one more on init because of table headers
    if (start == 0) {
        end += 1;
    }
    const file_id = document.querySelector('#filename').dataset.fileId
    counter = end + 1;
    fetch(`/file_rows?file_id=${file_id}&start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => add_rows(data.rows, start))
};

function add_rows(rows, start) {
    const tbody = document.querySelector('table tbody')
    rows.forEach((row,index) => {
        tr = document.createElement('tr');
        row.forEach(value => {
            let td = document.createElement('td')
            td.innerHTML = value
            tr.append(td)
        })
        if (start == 0 && index == 0) {
            tr.className = 'table-info';
            document.querySelector('table thead').append(tr);
        }
        else {
            tr.className = 'table-secondary';
            tbody.append(tr)
        }
    });
    if (rows.length < quantity) {
        document.querySelector('#load').remove()
    }
    window.scrollTo(0, document.body.scrollHeight);
};