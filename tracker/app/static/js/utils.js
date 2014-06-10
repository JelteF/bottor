'use strict';

/* Redirect the user to a new page. */
function redirect(url) {
    window.location = url;
}

//---------------------- Flash messages ---------------------------------------
var $default_flash_element, $flash_element, messages_div;

$(function() {
    $default_flash_element = $('div.messages');
    $flash_element = $default_flash_element;
});

function flash(message, type) {
    messages_div = $flash_element.html() + '<div class="alert alert-' +
        type + '">' + message +'</div>\n';
    $flash_element.html(messages_div);
}

function clearflash() {
    messages_div = "";
    $flash_element.html("");
}

//---------------------- Form automation --------------------------------------
function set_form_values(model, $form) {
    var $input_fields = $form
            .find('.form-control, .form_timepicker, .form_select')
            .not('.select2-offscreen');
    var $select2 = $form.find('select.form_select.select2-offscreen');
    var $check_boxes = $form.find('.form_check');
    var $radio_buttons = $form.find('input.form_radio:checked');
    var $datepicker = $form.find('.form_datepicker:visible');

    _.forEach($input_fields, function(field) {
        var $field = $(field);
        model.set($field.data('property'), $field.val())
    });

    _.forEach($select2, function(box) {
        var $box = $(box);
        model.set($box.data('property'), $box.select2('val'))
    });

    _.forEach($check_boxes, function(box) {
        var $box = $(box);
        model.set($box.data('property'), $box.prop('checked'));
    });

    _.forEach($radio_buttons, function(rdo) {
        var $rdo = $(rdo);
        model.set($rdo.data('property'), $rdo.val());
    });

    _.forEach($datepicker, function(picker) {
        var $picker = $(picker);
        var date = moment($picker.val(), DUTCH_DATE).format(ISO_DATE);
        model.set($picker.data('property'), date);
    });
}

function ajax_error_handler(response, no_clear) {
    if (!no_clear) {
        clearflash();
    }

    var error_text = get_error_text(response);

    // 401 occurs when the user is not logged in else flash the error
    if (response.status == 401) {
        show_login(error_text);
    }
    else {
        flash(error_text, 'danger');
    }
}

/* Wrapper that automatically handlers error responses from a save call. */
function save_werr(obj, attrs, success) {
    obj.save(attrs, {
        success: success,
        error: function(model, response, options) {
            ajax_error_handler(response);
        }
    });
}
function destroy_werr(obj, success, button) {
    obj.destroy({
        success: success,
        error: function(model, response, options) {
            ajax_error_handler(response, button);
        }
    });
}

function get_error_text(response) {
    // Try getting the error text that was sent by the server
    try {
        return $.parseJSON(response.responseText).error;
    }
    catch(e) {
        return 'Er is een error voorgekomen die niet bekend was, laat dit ' +
            'weten aan de ICT mensen';
    }
}

/* Find the element's parent tr. */
function find_tr($element) {
    return $element.parents('tr');
}


/* Get object from json array */
function getObjects(obj, key, val) {
    var objects = [];
    for (var i in obj) {
        if (!obj.hasOwnProperty(i)) continue;
        if (typeof obj[i] == 'object') {
            objects = objects.concat(getObjects(obj[i], key, val));
        } else if (i == key && obj[key] == val) {
            objects.push(obj);
        }
    }
    return objects;
}