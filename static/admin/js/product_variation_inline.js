// Product Variation Inline JavaScript
(function($) {
    $(document).ready(function() {
        // Make sure the table doesn't overflow
        $('.field-productvariation_set .tabular').each(function() {
            var $table = $(this);
            $table.css({
                'width': '100%',
                'table-layout': 'auto',
                'word-wrap': 'break-word'
            });
            
            // Set max widths for input fields
            $table.find('input[type="text"], input[type="number"]').each(function() {
                var $input = $(this);
                var fieldName = $input.closest('td').attr('class');
                
                if (fieldName) {
                    if (fieldName.includes('field-name')) {
                        $input.css({
                            'max-width': '180px',
                            'min-width': '150px'
                        });
                    } else if (fieldName.includes('field-quantity')) {
                        $input.css('max-width', '100px');
                    } else if (fieldName.includes('field-unit')) {
                        $input.css('max-width', '60px');
                    } else if (fieldName.includes('field-price_modifier')) {
                        $input.css('max-width', '80px');
                    } else if (fieldName.includes('field-stock')) {
                        $input.css('max-width', '70px');
                    }
                }
            });
        });
        
        // Handle dynamically added rows
        $(document).on('formset:added', function(event, $row) {
            $row.find('input[type="text"], input[type="number"]').each(function() {
                var $input = $(this);
                var fieldName = $input.closest('td').attr('class');
                
                if (fieldName) {
                    if (fieldName.includes('field-name')) {
                        $input.css({
                            'max-width': '180px',
                            'min-width': '150px'
                        });
                    } else if (fieldName.includes('field-quantity')) {
                        $input.css('max-width', '100px');
                    } else if (fieldName.includes('field-unit')) {
                        $input.css('max-width', '60px');
                    } else if (fieldName.includes('field-price_modifier')) {
                        $input.css('max-width', '80px');
                    } else if (fieldName.includes('field-stock')) {
                        $input.css('max-width', '70px');
                    }
                }
            });
        });
    });
})(django.jQuery);

