document.addEventListener('DOMContentLoaded', function() {
    load_table();
});

function load_table() {
    const file_id = document.querySelector('#filename').dataset.fileId
    const body = JSON.stringify({"file_id": file_id})
    fetch("/value_count_table/", {
      method: "POST",
      body: body,
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
};
