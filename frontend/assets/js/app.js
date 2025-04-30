var sdk = apigClientFactory.newClient({});

function upload_photos() {
    var file_path = (document.getElementById('filename').value).split("\\");
    var file_name = file_path[file_path.length - 1];

    var file = document.getElementById('filename').files[0];

    var custom_labels = document.getElementById('custom_labels').value;

    var additional_params = {
        headers: {
        'Content-Type': file.type,
        'x-api-key': 'QtTlr0aoKn382w1ElTaJg6znh8JfK19x4CCEkJOt',
        'accept': 'application/json',
        'x-amz-meta-customLabels': custom_labels
        }
    }

    var url = 'https://s3.amazonaws.com/cs-gy-9223-b2/' + file_name;

    axios.put(url, file, additional_params).then(
        function (result) {
        console.log(result);
        }
    ).catch(function (result) {
        console.log(result);
    });
}

function search_photos() {
    var query = document.getElementById('query').value.trim().toLowerCase();

    if (!query) {
        alert('No query given')
    }
    else {
        search_endpoint = 'https://0uzkpejxec.execute-api.us-east-1.amazonaws.com/PhotoWebApp/search?q=${}'
    }
}