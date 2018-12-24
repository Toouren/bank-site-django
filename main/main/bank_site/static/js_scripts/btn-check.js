$.validator.addMethod('phone_rule', function (value, element) {
    return this.optional(element) || /^\+[0-9]\(([0-9]){3}\)([0-9]){3}-([0-9]){2}-([0-9]){2}$/.test(value);
}, "Please enter a valid phone number");

$.validator.addMethod('card_number_rule', function (value, element) {
    return this.optional(element) || /^\d{4}-\d{4}-\d{4}-\d{4}$/.test(value);
}, "Please enter a valid card number number");

$(document).ready(function () {
    $('#card-pay-form input').on('blur', function () {
        if ($('#card-pay-form').valid()) {
            $('#card-pay').prop('disabled', false);
            $('#card-pay').css({'cursor': 'pointer', 'opacity': '1'});
        }
    });

    $('#our-bank-form input').on('blur', function () {
        if ($('#our-bank-form').valid()) {
            $('#our-bank-pay').prop('disabled', false);
            $('#our-bank-pay').css({'cursor': 'pointer', 'opacity': '1'});
        }
    });

    $('#get-form input').on('blur', function () {
        if ($('#get-form').valid()) {
            $('#get-bank-pay').prop('disabled', false);
            $('#get-bank-pay').css({'cursor': 'pointer', 'opacity': '1'});
        }
    });

    $('#card-pay-form').validate({
        rules: {
            sum: {
                required: true,
                range: [1000, 75000],
                number: true
            },
            number: 'card_number_rule',
            date: {
                required: true,
                date: true
            },
            cvc: {
                required: true,
                rangelength: [3, 3]
            },
            comment: {
                required: true,
                maxlength: 150
            },
            email: {
                required: true,
                email: true
            }
        },

        errorPlacement: function(error, element) {
            return true;
        },

        highlight: function(element, errorClass, validClass) {
            $(element).css('border-bottom', '1px solid #E60000');
        },

        unhighlight: function(element, errorClass, validClass) {
            $(element).css('border-bottom', '1px solid rgb(68,157,47)');
        }
    });

    $('#our-bank-form').validate({
        rules: {
            our_payer: {
                required: true,
                rangelength: [10, 12],
                number: true
            },
            our_bik: {
                required: true,
                number: true,
                rangelength: [9, 9]
            },
            our_comment: {
                required: true,
                maxlength: 150
            },
            our_sum: {
                required: true,
                number: true,
                range: [1000, 75000]
            }
        },

        errorPlacement: function(error, element) {
            return true;
        },

        highlight: function(element, errorClass, validClass) {
            $(element).css('border-bottom', '1px solid #E60000');
        },

        unhighlight: function(element, errorClass, validClass) {
            $(element).css('border-bottom', '1px solid rgb(68,157,47)');
        }
    });

    $('#get-form').validate({
        rules: {
            get_requester: {
                required: true,
                rangelength: [10, 12],
                number: true
            },
            get_bik: {
                required: true,
                number: true,
                rangelength: [9, 9]
            },
            get_comment: {
                required: true,
                maxlength: 150
            },
            get_sum: {
                required: true,
                number: true,
                range: [1000, 75000]
            },
            get_phone: 'phone_rule',
            get_email: {
                required: true,
                email: true
            }
        },

        errorPlacement: function(error, element) {
            return true;
        },

        highlight: function(element, errorClass, validClass) {
            $(element).css('border-bottom', '1px solid #E60000');
        },

        unhighlight: function(element, errorClass, validClass) {
            $(element).css('border-bottom', '1px solid rgb(68,157,47)');
        }
    });
});