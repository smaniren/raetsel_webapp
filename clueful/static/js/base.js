/* Submit buttons */
function disableSubmitButton(form){
    submitButtons = form.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => button.innerHTML = 'Please wait...')
    submitButtons.forEach(button => button.disabled = true)
    return true;
};


