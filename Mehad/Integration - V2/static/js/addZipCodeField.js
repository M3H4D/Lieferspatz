function addZipCode() {
    const container = document.getElementById('zipCodeContainer');
    const input = document.createElement('input');
    input.type = 'text';
    input.name = 'delivery_zip_codes';
    input.placeholder = 'Enter delivery zip code';
    container.appendChild(input);
}