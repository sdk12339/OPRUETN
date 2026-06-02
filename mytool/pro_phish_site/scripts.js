
$(function() {
  $('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top - 100
        }, 1000);
        return false;
      }
    }
  });
});
/* mobile menu link */
var selected_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'CA', 'GB'];

$(document).ready(function($) {
	$(".menulink a").click(function() {
	console.log('this');
	  	$("#menu").slideToggle('fast');
	});
	if(selected_countries.indexOf($('#country_code').val()) == -1) {
    	$('#email-service-updates').hide();
    	$('#tos-accepted').hide();
		jQuery('#tos-accepted input').remove();
		jQuery('#email-service-updates input').remove()
		jQuery('#email_service_exists').val("");
    }else {
        $('#email-service-updates').show();
    	$('#tos-accepted').show();
		if(jQuery('#email-service-updates #email_service_updates').length == 0 ){
			jQuery('#email-service-updates').prepend('<input value="1" type="checkbox" name="email_service_updates" id="email_service_updates">');
			jQuery('#email_service_exists').val("1");
		}
		if(jQuery('#tos-accepted #tos_accepted').length == 0 ){
			jQuery('#tos-accepted').prepend('<input value="1" type="checkbox" name="tos_accepted" id="tos_accepted">');
		}
    }

	$('#country_code').change(function(){
	    if(selected_countries.indexOf($(this).val()) == -1) {
			$('#email-service-updates').hide();
			$('#tos-accepted').hide();
			jQuery('#tos-accepted input').remove();
			jQuery('#email-service-updates input').remove()
			jQuery('#email_service_exists').val("");
	    }else {
			$('#email-service-updates').show();
			$('#tos-accepted').show();
			if(jQuery('#email-service-updates #email_service_updates').length == 0 ){
				jQuery('#email-service-updates').prepend('<input value="1" type="checkbox" name="email_service_updates" id="email_service_updates">');
				jQuery('#email_service_exists').val("1");
			}
			if(jQuery('#tos-accepted #tos_accepted').length == 0 ){
				jQuery('#tos-accepted').prepend('<input value="1" type="checkbox" name="tos_accepted" id="tos_accepted">');
			}
	    }
	});
});

/* bug fix: show header menu buttons when window back to desktop size */

$(window).on('resize', function(){
      var win = $(this); //this = window
      if (win.width() >= 800) {
	  jQuery("#menu").show();
	  }
});


/* open close example code */

$(function() {
	$(".sample_button").click(function() {
	   $('.example').show();
	   $('.get_started').addClass('pulsating');
	   $('.index_tagline').show();
	   $(".sample_button").hide();
	});
});

$(".sample_button").click(function (event) {
     event.stopPropagation()
})

$(".example").click(function (event) {
     event.stopPropagation()
})

$(function() {
	$(document).click(function() {
	   $('.example').hide();
	   $('.get_started').removeClass('pulsating');
	   $('.index_tagline').hide();
	   $(".sample_button").show();
	});
});


/* credit card form */

  $(document).ready(function(){
    $("#credit_card").click(function(){
		$('.credit_card_form_container').slideDown(100);
		$('#pm_paypal').css("margin-top","20px");
		$('#pm_paypal').removeClass("no_border_top");
	});
	$( "#checkout-invoice-credit-card #credit_card" ).trigger( "click" );
  });


/* FAQ function */

$('.faq_row').click(function () {

	var $this = $(this);
    $(".faq_content").not($this.parent().next()).slideUp(100);
    $this.parent().next().slideToggle(100);
	$this.addClass("faq_row_current");
	$this.toggleClass("no_border_bottom_radius");
	$this.toggleClass("no_box_shadow");
});


/* toggle html text function ".toggleText()" */

$.fn.toggleText = function(t1, t2){
  if (this.text() == t1) this.text(t2);
  else                   this.text(t1);
  return this;
};


/* update show more/less function */

$('.action_bar').click(function () {

    var $this = $(this);
    $this.toggleClass("").prev().slideToggle(100);
    // $this.toggleClass("selected");
	$this.find(".show_more_button").toggleText("show less", "show more");
	$(".download_hover.secondary").toggleClass("no_border_bottom");

});

/* click to view more - system status details */

$('.open_ssdetails').click(function () {

    var $this = $(this);
    $this.toggleClass("").next().slideToggle(100);
	$this.find(".updated_note").toggleText("hide details", "click to view more");

});

/* expand - payment, usage */

$('.expand').find(".download_pdf_btn").click(function (event) {
     // stop the function below if clicked on "download_pdf_btn"
     event.stopPropagation()
})

$('.expand').click(function () {

    var $this = $(this);
    $this.toggleClass("").next().slideToggle(100);
    $this.toggleClass("selected");
	$this.find(".show_all_entries_button").toggleText("show all entries", "show less entries");
	$this.find(".view_invoice").toggleText("View", "Hide");

});

/* index - show currency change - currencies strip */

$('.currency_showcase').hover(function () {

    var $this = $(this);

	if($this.hasClass("up")){
       $this.toggleClass("progress_green");
	} else if($this.hasClass("down")) {
       $this.toggleClass("progress_red");
	}

	$this.find(".content_normal").toggleClass("hidden");
	$this.find(".content_hover").toggleClass("hidden");

});

$('.partners.hover_change_text').hover(function () {

	$("#header_text").toggleText("CHANGE - YESTERDAY (EOD) TO TODAY","168 CURRENCIES & PRECIOUS METALS");

});

/* index - numverify country code showcase */

$('.country_code_showcase').hover(function () {

    var $this = $(this);

	$this.find(".content_normal").toggleClass("hidden");
	$this.find(".content_hover").toggleClass("hidden");

});

$('.partners.hover_change_text.numverify').hover(function () {

	$("#header_text").toggleText("SUPPORTING 232 COUNTRIES","SEE ALL SUPPORTED COUNTRIES");

});

/* Change password form */

$(function() {
	$("#change_password_button").click(function() {
	   $('#change_password_form').show(0);
	   $('#change_password_placeholder').hide(0);
	   $('#change_password_button').hide(0);
	   $('#change_password_cancel').show(0);
	});
});

$(function() {
	$("#change_password_cancel").click(function() {
	   $('#change_password_form').hide(0);
	   $('#change_password_placeholder').show(0);
	   $('#change_password_button').show(0);
	   $('#change_password_cancel').hide(0);
	});
});

/* keep change password form opened after being submitted */

if($('#change_password_active').val() == '1')
{
	   $('#change_password_form').show(0);
	   $('#change_password_placeholder').hide(0);
	   $('#change_password_button').hide(0);
	   $('#change_password_cancel').show(0);
}


/* New Payment Method Form */

$(function() {
	$("#new_payment_method_button").click(function() {
	   $('#new_payment_method_container').slideToggle(0);
	   $("#new_payment_method_button").toggleText("ADD NEW", "CANCEL");
	   $("#get_mt60").toggleClass("mt60");
	   $( "#credit_card" ).trigger( "click" );
	});
});



/* show/hide Security Code hint */

$( "#get_sc_hint").hover(function() {

    $('img.sc_hint').toggleClass("visibility_hidden");

});

/* show/hide Download PDF */

$( ".hover_pdf").mouseover(function() {

    $('.download_hover').removeClass("visibility_hidden_actual");

});

$( ".hover_pdf").mouseout(function() {

    $('.download_hover').addClass("visibility_hidden_actual");

});


/* show/hide password footnote */

$( "#password_section").hover(function() {

    $('#password_footnote').toggleClass("color_transparent");

});


/* show/hide renews info */

$( ".hover_renews").hover(function() {

    $('.tick').toggleClass("hidden");
    $('.renews_info').toggleClass("hidden");

});

/* expand error types - documentation */

$( ".expand_table_button").click(function() {

    $(this).toggleText("show less","show more");
	$('tr.hidden').fadeToggle(200);

});


/* disable button after one click */

//for forms
$('form.one_click_only').one('submit', function(event) {
    $('label.one_click_only').css('pointer-events','none');
    $(this).find('label.one_click_only').html('loading...');
    $(this).find('label.one_click_only').css('opacity', '0.9');

});

//for anchors
$('a.one_click_only').one('click', function() {
	$(this).css('pointer-events', 'none');
    $(this).html('loading...');
    $(this).css('opacity', '1');
});


/* fade header in */

$(document).scroll(function() {
	if ($(this).scrollTop() > 1) {
    $('.header_action').removeClass("transparent");
    } else {
    $('.header_action').addClass("transparent");
	}
});

/* code box index */

function switchCode(id, className) {

$(".codebox_button.selected").removeClass("selected");
$("#open_code_" + id).addClass("selected");
$("." + className).hide();
$("#code_" + id).show();

}

/* mailboxlayer: hide/show score label on index */

$('#open_code_6').click(function(){
   $("#score_box").hide();
});
$('#open_code_5').click(function(){
   $("#score_box").show();
});


/* index links on mobile */

  $(document).ready(function(){

	var windowSize = $(window).width();

    if (windowSize < 800) {
       $("a.href_on_mobile").attr("href", "/product")
   }

  });


/* disable panel scroll on small height */

var callback = function(){
      var win = $(this); //this = window
      if (win.height() >= 1000) {
      $(".panels").css("overflow","scroll");
      $('.scroll_arrow.opacity').css("opacity","0");
	  $(".promo_target_box.content.plans").css("margin-top","-20px");
      $('.scroll_arrow').css("pointer-events","none");
	  $('.fourty_on_vert_res').css("padding-bottom","35px");
	   } else {
      $(".panels").css("overflow","hidden");
      $('.scroll_arrow.opacity').css("opacity","1");
	  $(".promo_target_box.content.plans").css("margin-top","0px");
      $('.scroll_arrow').css("pointer-events","auto");
	  $('.fourty_on_vert_res').css("padding-bottom","40px");
	   }
}

$(window).load(callback);
$(window).resize(callback);

/* GIFLAYER - DOCUMENTATION - SWITCH FPS EXAMPLE GIFS */

$(document).on('click', '[data-show-fps]', function(event) {
	"use strict";
	event.preventDefault();
	$('[data-fps]').hide();
	$('[data-show-fps]').removeClass('selected');
	$(this).addClass('selected');
	$('[data-fps="'+$(this).attr('data-show-fps')+'"]').fadeIn(150);
});

/* PDFLAYER - SWITCH OPTIONAL PARAMETERS */

$(document).on('change', 'select.optional_params', function() {
	"use strict";
	var paramID = $(this).val();

	$('[data-optional-parameter]').hide();
	$('[data-optional-parameter="'+paramID+'"]').show();

});

/* PDFLAYER - UNIVERSAL SELECT-ID SHOW HIDE */

$('body').on('change', '.select_show_hide', function() {
	"use strict";

	var type = $(this).attr('data-type');
	$('[data-type-group="'+type+'"]').hide();

	var show = $(this).val();
	$('[data-type-target="'+show+'"]').show();

});


/* NEW March 4 2018 - CONFIRMATION POPUP */
$('body').on('click', '[data-confirmation-popup]', function() {
	
	var action = $(this).attr('data-confirmation-popup');
	var htmlContent;

	var heading;
	var text;
	var actionButtonText;
	var actionButtonClass;
	var actionButtonHREF;
	var cancelButtonText;
	var footnote;

	switch (action) {

		case 'downgrade':

			heading = 'Downgrade';
			// text = 'Please confirm your downgrade to the '+$(this).closest('.plan').find('[data-plan-name]').attr('data-plan-name')+'. Your previous subscription plan will remain active until the end of the current period.';
			text = 'Please contact <a target="_blank" href="mailto:subscription@apilayer.com" class="blue_link">subscription@apilayer.com</a> with your downgrade reason and we would be happy to process your request accordingly.';
			actionButtonText = 'Downgrade Account';
			actionButtonClass = 'red_button';
			actionButtonHREF = $(this).attr('data-href');
			cancelButtonText = 'Cancel';
			footnote = '<p class="popup_footnote">Looking to change your payment frequency? Follow these <a target="_blank" href="/faq?change_payment_frequency=1#change_payment_frequency" class="blue_link">instructions</a>. </p>';

		break;

		case 'upgrade_monthly':
		case 'upgrade_yearly':

			heading = 'Upgrade';
			text = 'Please confirm your upgrade to the '+ ($(this).closest('.plan').find('[data-plan-name]').attr('data-plan-name')|| $(this).closest('.plan').find('[data-plan-name]').data('planName')|| $(this).closest('.plan').attr('data-plan-name')|| $(this).closest('.plan').find('.plan-title').text().trim()|| 'selected plan') + '. The remaining unused days of your current plan will be deducted from your new invoice amount.';
      actionButtonText = action === 'upgrade_monthly' ? '<select class="price_dropdown"><option class="price_option" value="monthly"> Pay $'+Number(($(this).closest('.plan').find('[data-monthly-price]').attr('data-monthly-price')*1).toFixed(2)).toLocaleString()+' per month</option></select>' : '<select class="price_dropdown"><option class="price_option" value="yearly"> Pay $'+Number(($(this).closest('.plan').find('[data-yearly-price]').attr('data-yearly-price')*1).toFixed(2)).toLocaleString()+' per year</option></select>'
			actionButtonHREF = $(this).attr('data-href');
			cancelButtonText = 'Cancel';
			footnote = '<p class="popup_footnote">Looking to change your payment frequency? Follow these <a target="_blank" href="/faq?change_payment_frequency=1#change_payment_frequency" class="blue_link">instructions</a>. </p>';

		break;

		case 'upgrade_choose_frequency':

			platinum_support_popup = ''
			actionButtonHREF = $(this).attr('data-href');
			platinum_support_active = $('#platinum_support_active_status').val() == "1" ? 'onclick="return false"' : '';
			platinum_choosed = $(this).closest('.plan').find('[data-platinum-choosed]').attr('data-platinum-choosed');
			platinum_choosed == "1" || platinum_support_active ? platinum_checked = 'checked=""' : platinum_checked = '';
			annualPlatinumPrice = $(this).closest('.plan').find('[data-platinum-price]').attr('data-platinum-price');
			if(annualPlatinumPrice > 0){
				platinum_support_popup = '<div class="platinum_support_popup"><label for="platinum_support" class="platinum_label"><input type="checkbox" name="is_platinum_support" value="1" id="platinum_support_check"' + platinum_support_active + platinum_checked +'> Platinum Support - Pay $' + annualPlatinumPrice + ' billed annually</label></div>';
			}
			htmlContent = '<div class="cd-popup is-visible new_confirmation_popup choose_payment_freq" role="alert"> <div class="cd-popup-container upgrade-popup-box upgrade_popup"> <p class="no_min_width"><span class="cd-heading">Upgrade</span>Please confirm your upgrade by choosing your billing frequency. </p> <select class="price_dropdown"> <option class="price_option" value="monthly"> Pay $'+Number(($(this).closest('.plan').find('[data-monthly-price]').attr('data-monthly-price')*1).toFixed(2)).toLocaleString()+' per month</option><option class="price_option" value="yearly"> Pay $'+Number(($(this).closest('.plan').find('[data-yearly-price]').attr('data-yearly-price'))).toLocaleString()+' per year <span class="small_and_fat green"> -'+ $(this).closest('.plan').find('[data-discount-percentage]').attr('data-discount-percentage') +'%</span></option></select> '+ platinum_support_popup +' <a href="'+actionButtonHREF+'" onclick="set_platinum_support()" style="color: green !important;" class="cd-popup-close popup_button no platinum_upgrade">Upgrade</a> <a href="javascript:void(0)" class="cd-popup-close popup_button no">Cancel</a> </div></div>';

		break;

    case 'upgrade_platinum_support_common':
    case 'upgrade_platinum_support_only':
      actionButtonHREF = $(this).attr('data-href');
      heading = 'Upgrade';
      text = 'Please confirm your upgrade to the Platinum Support';
    break;
	}

	if (!htmlContent) {

	// htmlContent = '<div class="cd-popup is-visible new_confirmation_popup" role="alert"> <div class="cd-popup-container pop-up-cotainer"> <p class="no_min_width"><span class="cd-heading">'+heading+'</span>'+text+'</p>';
    htmlContent = '<div class="cd-popup is-visible new_confirmation_popup" role="alert"> <div class="cd-popup-container only_platinum upgrade_popup"> <p class="no_min_width"><span class="cd-heading">'+heading+'</span>'+text+'</p>';
//   if($('#portal_id').val() == '27' || $('#portal_id').val() == '1' || $('#portal_id').val() == '16'){
//   	var displayReason = $(this).attr('id');
//   	htmlContent += '<div class="issue-radio" style="display:'+(displayReason ? displayReason.toLowerCase() == 'free' ? 'block' : 'none' : 'none')+'"><p class="enter-reason">Please select the reason for downgrading your plan below:</p><label class="ratio-btn">Technical issues<input type="radio" checked="checked" name="reason" value="technical_issues"><span class="checkmark"></span></label><label class="ratio-btn"> Too expensive<input type="radio" checked="checked" name="reason" value="too_expensive"><span class="checkmark"></span></label><label class="ratio-btn">Missing features I need<input type="radio" checked="checked" name="reason" value="missing_features"><span class="checkmark"></span></label><label class="ratio-btn">Switching to another product<input type="radio" checked="checked" name="reason" value="switching_to_another_product"><span class="checkmark"></span></label><label class="ratio-btn">Not sure how to use the service<input type="radio" checked="checked" name="reason" value="not_sure_how_to_use_it"><span class="checkmark"></span></label><label class="ratio-btn">Change in business requirements<input type="radio" checked="checked" name="reason" value="change_in_business_requirements"><span class="checkmark"></span></label><label class="ratio-btn">Other (please specify) <input type="radio" checked="checked" name="reason" value="other"><span class="checkmark"></span></label><div class="character-blk textarea-control"><div class="char-label" id="other_text_chars">30 characters left</div><textarea rows="2" cols="50" placeholder="" class="enter-text" name="other_text" id="other_text" maxlength="30" onkeyup="countChar(\'other_text\', 30)"></textarea><span class="error" style="display:none">Please enter other reason.</span></div><div class="custom-label character-blk textarea-control"><label>Anything else youd like to share</label><textarea rows="5" cols="50" placeholder="" class="enter-text description-area" name="comment" id="comment" maxlength="200" onkeyup="countChar(\'comment\', 200)"></textarea><div class="char-label" id="comment_chars">200 characters left</div></div></div>'+`<script>$('input[name=reason]').change(function(){
//     		$('#other_text').val('');
//     		if(typeof countChar == 'function'){
//         	countChar('other_text', 30);
//     		}
//     		if($( 'input[name=reason]:checked' ).val() == 'other'){
//         	$('#other_text').show();
//         	$('#other_text_chars').show();
//         	$('#other_text').data('required', 'true');
//     		}
//     		else{
//         	$('#other_text').data('required', 'false');
//         	$('#other_text').hide();
//         	$('#other_text_chars').hide();
//         	$('.error').hide();
//     		}
// 			});</script>`;
//   }
	switch (action) {

		case 'downgrade':
			htmlContent += '<div class="yes_no_buttons_container">  <a href="javascript:void(0)" class="cd-popup-close popup_button no">Cancel</a></div> </div></div>';
		break;

		case 'upgrade_monthly':
		case 'upgrade_yearly':

      annualPlatinumPrice = $(this).closest('.plan').find('[data-platinum-price]').attr('data-platinum-price');
	  platinum_support_active = $('#platinum_support_active_status').val() == "1" ? 'onclick="return false"' : '';
	  platinum_choosed = $(this).closest('.plan').find('[data-platinum-choosed]').attr('data-platinum-choosed');
	  platinum_choosed == "1" || platinum_support_active ? platinum_checked = 'checked=""' : platinum_checked = '';
	  
			htmlContent += '<div class="yes_no_buttons_container">'+actionButtonText+'<div class="platinum_support_popup"><label for="platinum_support" class="platinum_label"><input type="checkbox" name="is_platinum_support" value="1" id="platinum_support_check"' + platinum_support_active + platinum_checked +'> Platinum Support - Pay $' + annualPlatinumPrice + ' billed annually</label></div><a href="'+actionButtonHREF+'" onclick="set_platinum_support()" style="color: green !important;" class="cd-popup-close popup_button no platinum_upgrade">Upgrade</a><a href="javascript:void(0)" class="cd-popup-close popup_button no">Cancel</a> '+footnote+'</div> </div></div>';
		break;

    case 'upgrade_platinum_support_common':
      annualPlatinumPrice = $(this).attr('data-platinum-price');
      platinum_choosed = $(this).attr('data-platinum-choosed');
      platinum_checked = 'checked=""';
      htmlContent += '<div class="yes_no_buttons_container"><div class="platinum_support_popup"><label for="platinum_support" class="platinum_label"><input type="checkbox" name="is_platinum_support" value="1" id="platinum_support_check_new" onclick="return false"'+ platinum_checked +'> Platinum Support - Pay $' + annualPlatinumPrice + ' billed annually</label></div><a href="'+actionButtonHREF+'" onclick="set_platinum_support_common()" style="color: green !important;" class="cd-popup-close popup_button no platinum_upgrade_new">Upgrade</a><a href="javascript:void(0)" class="cd-popup-close popup_button no">Cancel</a></div> </div></div>';
    break;

    case 'upgrade_platinum_support_only':
      annualPlatinumPrice = $(this).closest('.plan').find('[data-platinum-price]').attr('data-platinum-price');
      platinum_choosed = $(this).closest('.plan').find('[data-platinum-choosed]').attr('data-platinum-choosed');
      platinum_checked = 'checked=""';
      htmlContent += '<div class="yes_no_buttons_container"><div class="platinum_support_popup"><label for="platinum_support" class="platinum_label"><input type="checkbox" name="is_platinum_support" value="1" id="platinum_support_check" onclick="return false"'+ platinum_checked +'> Platinum Support - Pay $' + annualPlatinumPrice + ' billed annually</label></div><a href="'+actionButtonHREF+'" onclick="set_platinum_support()" style="color: green !important;" class="cd-popup-close popup_button no platinum_upgrade">Upgrade</a><a href="javascript:void(0)" class="cd-popup-close popup_button no">Cancel</a></div> </div></div>';
    break;

} 
// 	htmlContent += '<div class="yes_no_buttons_container"> <a id="downgrade_button" href="'+actionButtonHREF+'" onclick="change_plan(this, event)" class="popup_button yes '+actionButtonClass+'">'+actionButtonText+'</a> <a href="javascript:void(0)" class="cd-popup-close popup_button no">Cancel</a> '+footnote+'</div> </div></div>';
	}

	$('body').append(htmlContent);
	if (typeof displayReason !== 'undefined') {
		if(displayReason && displayReason.toLowerCase() == 'free'){
			$('#other_text').data('required', 'true');
		}
	}
});

/* CLOSE CONFIRMATION POPUP */
$('body').on('click', '.cd-popup-close', function() {

	if ($(this).closest('.new_confirmation_popup').length > 0) {

		$(this).closest('.new_confirmation_popup').remove();

	}

});

/* send platinum support selection to backend*/
function set_platinum_support() {
  is_platinum_support = $('#platinum_support_check').is(":checked") === true ? 1 : 0;
  base_href = $('.platinum_upgrade').attr('href');
  frequency = $('.price_dropdown :selected').val();
  if (!base_href.includes('monthly') && !base_href.includes('yearly')) {
    base_href = base_href + frequency;
  }
  $('.platinum_upgrade').attr('href', base_href+'&is_platinum_support='+is_platinum_support);
}

function set_platinum_support_common() {
  base_href = $('.platinum_upgrade_new').attr('href');
  is_platinum_support = $('#platinum_support_check_new').is(":checked") === true ? 1 : 0;
  $('.platinum_upgrade_new').attr('href', base_href+'&is_platinum_support='+is_platinum_support);
}

function change_plan(val, evt){
	var reason = $('.issue-radio').is(':visible') ? $("input[type='radio'][name='reason']:checked").val() : '';
  var other_text = $('.issue-radio').is(':visible') ? $('#other_text').val() : '';
  var comment = $('.issue-radio').is(':visible') ? $('#comment').val() : '';
  if(!$('#other_text').data('required') || $('#other_text').data('required') == 'false' || $('#other_text').val().trim() != ''){
		document.getElementById("downgrade_button").href = val.getAttribute('href')+'&reason='+reason+'&other_text='+other_text+'&comment='+comment;
  }else{
    $('.error').show();
    evt.preventDefault();
  }
}

function countChar(id, maxlength) {
	let val = $('#'+id).val();
  let len = val.length;
  if (len > maxlength) {
    val = val.substring(0, maxlength);
  } else {
  	let msg = ' character'+(maxlength - len > 1 ? 's':'')+' left';
    $('#'+id+'_chars').text(maxlength - len + msg);
  }
  if(id =='other_text' && len > 0 && $('#'+id).next('.error').is(':visible')){
	  $('#'+id).next('.error').hide();
	}
};

function checboxDisplay(id) {
	var $checked = document.getElementById('other'+id);
	var $textbox = document.getElementById('textBox'+id);
	if($textbox && $checked) {
		$textbox.style.display = $checked.checked == true ? 'block' : 'none';
	}	
}

/* STRIPE PAYMENT 2019 - STRIPE INIT AND SUBMIT */
var stripe;
var elements;
var cardElement;
var cardButton;
var clientSecret;

// default Stripe action is charging existing cc
var StripeAction = $('body').find('[name="stripe_action"]').val();

function initStripe() {
	// init Stripe
	stripe = Stripe(window.stripePublishableKey);

	switch (StripeAction) {

	  case 'add_cc_only':
	  StripeActionCardSetup();
	  break;

	  case 'add_cc_and_charge':
	  StripeActionCardPayment();
	  break;

	  default:
	  // do nothing
	  break;

	}

}

function portalLink(portalId) {
	websiteURL = '';
	if(portalId == '32') {
		websiteURL = "https://exchangeratesapi.io";
	}
	else if(portalId == '16') {
		websiteURL = "https://ipstack.com";
	}
	else if(portalId == '33') {
		websiteURL = "https://countrylayer.com";
	}
	else if(portalId == '38') {
		websiteURL = "https://shippingdataapi.com/";
	}
	return websiteURL;
}


/* STRIPE ACTION CHARGE EXISTING CARD */
$('body').on('click', '#charge_existing_cc', function(event) {

	var chosenPaymentMethod = $('body').find('[name="choose_payment_option"]:checked');
	var paymentMethodID;

	clientSecret = chosenPaymentMethod.attr('data-secret');
	paymentMethodID = chosenPaymentMethod.attr('data-stripe-id');

	// only prevent standard paylane submission if stripe params present
	if (paymentMethodID && clientSecret) {
		event.preventDefault();
	} else {
		$('form[name="charge_existing_or_switch_pm"]').submit();
		return false;
	}

	initStripe();
	cardButton = $(this);

	$(this).addClass('loading');
	$(this).text('Loading ...');

	stripe.handleCardPayment(
	  clientSecret,
	  { payment_method: paymentMethodID }
	).then(function(result) {

	  if (result.error) {

		  $(cardButton).removeClass('loading');
		  $(cardButton).text('Try again');

		  // report error
		  dynamicInfo('error', 'Error: '+result.error.message+' (Code: "'+result.error.code+'")');
		  console.log(result.error);

	  } else {

		  // call to ajax handler to save credit card
		  var postData = {
			  paymentintent_id: $('body').find('#card-button').attr('data-payment-intent-id')
		  };

		  var postDataJSON = JSON.stringify(postData);
		  //console.log(postDataJSON);

		  $.ajax({
			  type: 'POST',
			  url: '/php/advanced_ajax_handler.php?type=stripe_capture_invoice_payment',
			  dataType: 'json',
			  data: ({ postArray: postDataJSON }),
			  success: function(json) {

				  if (json.success == 1) {

					portalId = $('#portal_id').val();
					planName = $('#plan_name').val();
					onlyPlatinumSupport = $('#only_platinum_support').val();
					
					if(onlyPlatinumSupport) {
						window.location.replace(portalLink(portalId)+"/thank-you-platinum-support");
						return;
					}
					switch (planName) {

						case 'Starter':
							window.location.replace(portalLink(portalId)+"/thank-you-starter");
						break;
					
						case 'Standard':
						case 'Basic':
							window.location.replace(portalLink(portalId)+"/thank-you-basic");
						break;
						
						case 'Business':
							window.location.replace(portalLink(portalId)+"/thank-you-business");
						break;

						case 'Professional':
							window.location.replace(portalLink(portalId)+"/thank-you-professional");
						break;
					
						case 'Business Pro':
							window.location.replace(portalLink(portalId)+"/thank-you-business-pro");
						break;
						
						case 'Professional Plus':
							window.location.replace(portalLink(portalId)+"/thank-you-pro-plus");
						break;
						case 'Enterprise':
							window.location.replace(portalLink(portalId)+"/thank-you-enterprise");
						break;
						case 'Enterprise+':
							window.location.replace(portalLink(portalId)+"/thank-you-enterprise-plus");
						break;
					
						default:
							window.location.replace(portalLink(portalId)+"/thank-you-free-api");
						break;
					}

				  } else {

				  	  dynamicInfo('error', 'An error occurred. Please try again or contact support.');

					  $(cardButton).removeClass('loading');
					  $(cardButton).text('Try again');

				  }

			  }

		  });

	  }

	});

});



/* STRIPE ACTION ADD CARD WITHOUT CHARGING */
function StripeActionCardSetup() {

	elements = stripe.elements({
	// force english
	locale: 'en',
	});

	cardElement = elements.create('card');
	cardElement.mount('#card-element');
	cardButton = document.getElementById('card-button');
	clientSecret = cardButton.dataset.secret;

	cardButton.addEventListener('click', function(ev) {

	  $(cardButton).addClass('loading');
	  $(cardButton).text('Loading ...');

		stripe.handleCardSetup(
		  clientSecret, cardElement, {}
		).then(function(result) {

		  if (result.error) {

			  $(cardButton).removeClass('loading');
			  $(cardButton).text('Try again');

			  // report error
			  dynamicInfo('error', 'Error: '+result.error.message+' (Code: "'+result.error.code+'")');
			  console.log(result.error);

		  } else {

			  // call to ajax handler to save credit card
			  var postData = {
				  setup_intent_id: $('body').find('#card-button').attr('data-setup-intent-id')
			  };

			  var postDataJSON = JSON.stringify(postData);
			  //console.log(postDataJSON);

			  $.ajax({
				  type: 'POST',
				  url: '/php/advanced_ajax_handler.php?type=add_stripe_payment_profile',
				  dataType: 'json',
				  data: ({ postArray: postDataJSON }),
				  success: function(json) {

					  if (json.success == 1) {

						  // reload page if card saved successfully
						  window.location.reload();
						  window.location.href = window.location.href + '?card_added=1';

					  } else {

					  	  dynamicInfo('error', 'An error occurred. Please try again or contact support.');

						  $(cardButton).removeClass('loading');
						  $(cardButton).text('Try again');

					  }

				  }

			  });

		  }

		});

	});

}


/* STRIPE ACTION ADD CARD WITH CHARGING */
function StripeActionCardPayment() {

	elements = stripe.elements({
	// force english
	locale: 'en',
	});

	cardElement = elements.create('card');
	cardElement.mount('#card-element');
	cardButton = document.getElementById('card-button');
	clientSecret = cardButton.dataset.secret;

	cardButton.addEventListener('click', function(ev) {

	  $(cardButton).addClass('loading');
	  $(cardButton).text('Loading ...');

	  stripe.handleCardPayment(
		clientSecret, cardElement, {
		  // not sending any payment_method_data here
		  payment_method_data: {}
		}
	  ).then(function(result) {

		if (result.error) {

			$(cardButton).removeClass('loading');
			$(cardButton).text('Try again');

			// report error
			dynamicInfo('error', 'Error: '+result.error.message+' (Code: "'+result.error.code+'")');
			console.log(result.error);

		} else {

			// call to ajax handler to save credit card
			var postData = {
				paymentintent_id: $('body').find('#card-button').attr('data-payment-intent-id')
			};

			var postDataJSON = JSON.stringify(postData);
			//console.log(postDataJSON);

			$.ajax({
				type: 'POST',
				url: '/php/advanced_ajax_handler.php?type=stripe_capture_invoice_payment',
				dataType: 'json',
				data: ({ postArray: postDataJSON }),
				success: function(json) {

					if (json.success == 1) {

						// redirect to thank you pages 
						portalId = $('#portal_id').val();
						planName = $('#plan_name').val();
						switch (planName) {

							case 'Starter':
							window.location.replace(portalLink(portalId)+"/thank-you-starter");
							break;
					
							case 'Standard':
							case 'Basic':
								window.location.replace(portalLink(portalId)+"/thank-you-basic");
							break;
							
							case 'Business':
								window.location.replace(portalLink(portalId)+"/thank-you-business");
							break;

							case 'Professional':
								window.location.replace(portalLink(portalId)+"/thank-you-professional");
							break;
						
							case 'Business Pro':
								window.location.replace(portalLink(portalId)+"/thank-you-business-pro");
							break;

							case 'Professional Plus':
								window.location.replace(portalLink(portalId)+"/thank-you-pro-plus");
							break;
							case 'Enterprise':
								window.location.replace(portalLink(portalId)+"/thank-you-enterprise");
							break;
							case 'Enterprise+':
								window.location.replace(portalLink(portalId)+"/thank-you-enterprise-plus");
							break;
						
							default:
								window.location.replace(portalLink(portalId)+"/thank-you-free-api");
							break;
						}

					} else {

				  	  	dynamicInfo('error', 'An error occurred. Please try again or contact support.');

						$(cardButton).removeClass('loading');
						$(cardButton).text('Try again');

					}

				}

			});

		}

	  });

	});

}


/* STRIPE PAYMENT 2019 - GET PAYMENT INTENT CLIENT SECRET */
$('body').on('click', '[data-stripe-action="get_client_secret"]', function() {

	// remove action attribute to prevent multiple calls to ajax handler
	$(this).removeAttr('data-stripe-action');

	// if action is only adding cc, get setup intent
	if (StripeAction === 'add_cc_only') {

		$.ajax({
			url: '/php/advanced_ajax_handler.php?type=stripe_create_setupintent',
			dataType: 'json',
			success: function(json) {

				// add client secret to relevant data attr
				$('body').find('#card-button').attr('data-secret', json.message.client_secret);
				$('body').find('#card-button').attr('data-setup-intent-id', json.message.id);

				initStripe();

			}

		});

	} else {

		// otherwise just initiate Stripe
		initStripe();

	}

});



/* DYNAMIC ERRORS */
function dynamicInfo(type, content, remove) {

	$('body').find('.dynamic_info').hide().html('');

	if (remove == 'true') {
	return false;
	}

	$('body').find('.dynamic_info').show().addClass(type).html('<p>'+content+'</p>');
	$("html, body").animate({ scrollTop: 0 });

}


/* Progress bar Js */

$(document).ready(function($) {
	if (typeof php_var !== 'undefined') {
		if (php_var <= 50) {

			$('#progress_bar_actual').addClass("progress_green");

		} else if ((php_var > 50) && (php_var <= 75)) {

			$('#progress_bar_actual').addClass("progress_yellow");

		} else if ((php_var > 75) && (php_var <= 90)) {

			$('#progress_bar_actual').addClass("progress_orange");

		} else if (php_var > 90) {

			$('#progress_bar_actual').addClass("progress_red");
		}
	}
});