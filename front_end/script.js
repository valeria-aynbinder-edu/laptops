async function load_laptops_data() {
    var requestOptions = {
      method: 'GET',
    };

    fetch("http://127.0.0.1:8000/laptops/api/stats/totals")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not OK');
            }
            return response.json()
        })
        .then(jsonContent => {
            console.log(jsonContent)
            document.getElementById("customers_stats").innerHTML = JSON.stringify(jsonContent)
        })
        .catch(error => console.log('error', error));
}


//open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security

