$.fn.datetimepicker.defaults.i18n.wagtail_custom_locale = {
    months: wagtailConfig.STRINGS.MONTHS,
    dayOfWeek: wagtailConfig.STRINGS.WEEKDAYS,
    dayOfWeekShort: wagtailConfig.STRINGS.WEEKDAYS_SHORT,
};
$.datetimepicker.setLocale('wagtail_custom_locale');

// Compare two date objects. Ignore minutes and seconds.
function dateEqual(x, y) {
    return x.getDate() === y.getDate() &&
           x.getMonth() === y.getMonth() &&
           x.getYear() === y.getYear()
}

/*
Remove the xdsoft_current css class from markup unless the selected date is currently in view.
Keep the normal behaviour if the home button is clicked.
 */
function hideCurrent(current, input) {
    var selected = new Date(input[0].value);
    if (!dateEqual(selected, current)) {
        $(this).find('.xdsoft_datepicker .xdsoft_current:not(.xdsoft_today)').removeClass('xdsoft_current');
    }
}

function DateChooser(id, opts) {
    if (window.dateTimePickerTranslations) {
        $('#' + id).datetimepicker($.extend({
            closeOnDateSelect: true,
            timepicker: false,
            scrollInput: false,
            format: 'd/m/Y',
            onGenerate: hideCurrent,
            onChangeDateTime: function(_, $el) {
              $el.get(0).dispatchEvent(new Event('change'))
            }
        }, opts || {}));
    } else {
        $('#' + id).datetimepicker($.extend({
            timepicker: false,
            scrollInput: false,
            format: 'd/m/Y',
            onGenerate: hideCurrent,
            onChangeDateTime: function(_, $el) {
              $el.get(0).dispatchEvent(new Event('change'))
            }
        }, opts || {}));
    }
}

function TimeChooser(id) {
    if (window.dateTimePickerTranslations) {
        $('#' + id).datetimepicker({
            closeOnDateSelect: true,
            datepicker: false,
            scrollInput: false,
            format: 'H:i',
            onChangeDateTime: function(_, $el) {
              $el.get(0).dispatchEvent(new Event('change'))
            }
        });
    } else {
        $('#' + id).datetimepicker({
            datepicker: false,
            format: 'H:i',
            onChangeDateTime: function(_, $el) {
              $el.get(0).dispatchEvent(new Event('change'))
            }
        });
    }
}

function DateTimeChooser(id, opts) {
    if (window.dateTimePickerTranslations) {
        $('#' + id).datetimepicker($.extend({
            closeOnDateSelect: true,
            format: 'd/m/Y H:i',
            scrollInput: false,
            onGenerate: hideCurrent,
            onChangeDateTime: function(_, $el) {
              $el.get(0).dispatchEvent(new Event('change'))
            }
        }, opts || {}));
    } else {
        $('#' + id).datetimepicker($.extend({
            format: 'd/m/Y H:i',
            onGenerate: hideCurrent,
            onChangeDateTime: function(_, $el) {
              $el.get(0).dispatchEvent(new Event('change'))
            }
        }, opts || {}));
    }
}

$(document).ready(function(){
    $('.date_time_input').each(function(){ var ids = $(this).find('input').attr('id'); DateTimeChooser(ids, {"dayOfWeekStart": 0, format: "d/m/Y H:i:s"});})
    $('.date_input').each(function(){ var ids = $(this).find('input').attr('id'); DateChooser(ids, {"dayOfWeekStart": 0, format: "d/m/Y"});})
    setInterval(function(){
        if($('.upload-complete')[0] != undefined){
            $('.date_time_input').each(function(){ var ids = $(this).find('input').attr('id'); DateTimeChooser(ids, {"dayOfWeekStart": 0, format: "d/m/Y H:i:s"});})
            $('.date_input').each(function(){ var ids = $(this).find('input').attr('id'); DateChooser(ids, {"dayOfWeekStart": 0, format: "d/m/Y"});}) 
        }
    }, 1000)

    $('.add-related').click(function(e){
        e.preventDefault()
        var url = $(this).attr('href')
        window.open(url, "Add New", "width=1400,height=800");
    })  

    try{
        $("[id$='validity_end']").val('')
        $("[id$='expiration_at']").val('')
    }catch(ex){}  
})
