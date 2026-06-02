function syncStateField() {
    const countries = JSON.parse(document.getElementById('countries').innerHTML)
        let stateInput = $('input.state')
        let stateLabel = $('label.state-label')
        let stateSelect = $('select.state-select')
        let stateSelectLabel = $('label.state-select-label')
        let currentState = (stateSelect.val() || stateInput.val() || "").trim();

        stateSelect.hide()
        stateSelectLabel.hide()

        
        let country = ($(".country_code").find("option:selected").text() || "").trim()
        let states = countries[country]

        if(states !== undefined) {
            stateInput.hide()
            stateLabel.hide()
            stateSelect.show()
            stateSelectLabel.show()

            stateInput.val('')
            stateSelect.find('option').remove()
            stateSelect.prop('required', true);
            stateSelect.append(new Option('Select a state', ''))

            $.each(states, (key, val) => {
                stateSelect.append(new Option(val, val))
            });
            if (currentState && stateSelect.find('option[value="' + currentState + '"]').length) {
               stateSelect.val(currentState);
            }
        }else{
            stateInput.show()
            stateLabel.show()
            stateSelect.hide()
            stateSelectLabel.hide()

            stateSelect.find('option').remove()
            stateSelect.prop('required', false);
        }
}

$(document).ready(function() {
    syncStateField();
    $('.country_code').on('change', function() {
        syncStateField();
    });
});