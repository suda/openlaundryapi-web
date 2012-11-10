(function ($) {

    $(document).ready(function () {
        $('.dateinput').datepicker({
            format: 'dd.mm.yyyy',
            weekStart: 1
        });
        $('.timeinput').timepicker({
            showSeconds: false,
            defaultTime: 'value',
            showMeridian: false
        });
    });

})(jQuery);
