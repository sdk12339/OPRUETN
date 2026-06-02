function openPopup(id, event) {

 event.preventDefault(); //prevents browser from following any a href=""
 $(id).show();
 $(id).addClass('is-visible');
 $(id).css("z-index", "999999999999999999999999");
 $(".reason-required").hide();
 let formId = id.replace('#popup','');
 formId = (formId == "Cancel") ? 0 : formId; //To reset the cancel subscription form
 $('.enter-text').removeAttr('style');


 let $textarea_comment = document.getElementById('comment' + formId);
    if($textarea_comment) {
        $textarea_comment.value = '';
        $textarea_comment.dispatchEvent(new Event('keyup'));
        $("#downgrade_plan" + formId).get(0).reset();
        $('.reason-required').hide();
    }
 }


jQuery(document).ready(function($){


//close popup
$('.cd-popup').on('click', function(event){
    if( $(event.target).is('.cd-popup-close') || $(event.target).is('.cd-popup') ) {
        event.preventDefault();
        $(this).hide();
    }
});

});

// Function to handle checkbox change
function handleCheckboxChange() { $(".reason-required").hide();}

// Add onchange event listener to each checkbox
document.querySelectorAll('.issue-radio input[type="checkbox"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', handleCheckboxChange);
});
