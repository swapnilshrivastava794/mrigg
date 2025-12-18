// Product Variation Inline JavaScript
(function($) {
    $(document).ready(function() {
        // Debug: Uncomment to verify script is loading
        // console.log('Product Variation Inline JS loaded');
        // Hide the original column completely to prevent overlap
        function hideOriginalColumn() {
            $('.field-productvariation_set .tabular th.original, .field-productvariation_set .tabular td.original').each(function() {
                $(this).css({
                    'display': 'none',
                    'width': '0',
                    'padding': '0',
                    'margin': '0',
                    'border': 'none'
                });
            });
        }
        
        // Hide original column immediately
        hideOriginalColumn();
        
        // Make sure the table doesn't overflow
        $('.field-productvariation_set .tabular').each(function() {
            var $table = $(this);
            $table.css({
                'width': '100%',
                'table-layout': 'fixed',
                'word-wrap': 'break-word'
            });
            
            // Hide original column for this table
            hideOriginalColumn();
            
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
        
        // Hide original column when DOM changes (for dynamically added content)
        var observer = new MutationObserver(function(mutations) {
            hideOriginalColumn();
        });
        
        // Observe changes to the inline group
        $('.field-productvariation_set').each(function() {
            observer.observe(this, { childList: true, subtree: true });
        });
        
        // Function to convert text to slug
        function slugify(text) {
            if (!text) return '';
            return text.toString().toLowerCase()
                .replace(/\s+/g, '-')           // Replace spaces with -
                .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
                .replace(/\-\-+/g, '-')         // Replace multiple - with single -
                .replace(/^-+/, '')             // Trim - from start of text
                .replace(/-+$/, '');            // Trim - from end of text
        }
        
        // Auto-populate slug from name field - Multiple methods for reliability
        function autoPopulateSlug($nameInput) {
            var nameValue = $nameInput.val();
            if (!nameValue) return;
            
            var slugValue = slugify(nameValue);
            var $row = $nameInput.closest('tr');
            var $slugInput = null;
            var found = false;
            
            // Method 1: Find by ID pattern (most reliable for Django admin)
            var idAttr = $nameInput.attr('id');
            if (idAttr) {
                // Try different ID patterns: id_variations-0-name or variations-0-name
                var match = idAttr.match(/(?:id_)?variations-(\d+)-name/);
                if (match) {
                    var rowIndex = match[1];
                    // Try multiple ID patterns
                    var patterns = [
                        'input[id*="id_variations-' + rowIndex + '-slug"]',
                        'input[id*="variations-' + rowIndex + '-slug"]',
                        'input[id$="variations-' + rowIndex + '-slug"]'
                    ];
                    
                    for (var i = 0; i < patterns.length; i++) {
                        $slugInput = $(patterns[i]);
                        if ($slugInput.length) {
                            $slugInput.val(slugValue);
                            found = true;
                            break;
                        }
                    }
                }
            }
            
            if (found) return;
            
            // Method 2: Find by field order - slug is 2nd visible column after name
            var $visibleTds = $row.find('td:visible');
            if ($visibleTds.length > 1) {
                // Find which td contains the name input
                $visibleTds.each(function(index) {
                    var $td = $(this);
                    if ($td.find($nameInput).length || $td.find('input').is($nameInput)) {
                        // Next td should be slug
                        if (index + 1 < $visibleTds.length) {
                            $slugInput = $($visibleTds[index + 1]).find('input');
                            if ($slugInput.length) {
                                var slugId = $slugInput.attr('id') || '';
                                if (slugId.indexOf('slug') !== -1 || !slugId) {
                                    $slugInput.val(slugValue);
                                    found = true;
                                    return false; // break
                                }
                            }
                        }
                    }
                });
            }
            
            if (found) return;
            
            // Method 3: Find by searching all inputs in row for slug
            $row.find('input').each(function() {
                var $input = $(this);
                var inputId = $input.attr('id') || '';
                if (inputId.indexOf('slug') !== -1) {
                    $input.val(slugValue);
                    found = true;
                    return false; // break
                }
            });
        }
        
        // Setup event handlers - comprehensive approach
        function setupSlugHandlers() {
            // Use event delegation for all name inputs
            $(document).on('input keyup', '.field-productvariation_set input[id*="-name"]', function(e) {
                autoPopulateSlug($(this));
            });
            
            // Also catch by class
            $(document).on('input keyup', '.field-productvariation_set td.field-name input', function(e) {
                autoPopulateSlug($(this));
            });
        }
        
        // Setup handlers on page load
        setupSlugHandlers();
        
        // Also setup for existing rows after a delay
        setTimeout(function() {
            $('.field-productvariation_set tbody tr').each(function() {
                var $row = $(this);
                // Try to find name input by ID first
                var $nameInput = $row.find('input[id*="-name"]');
                if (!$nameInput.length) {
                    // Fallback: find first text input in first visible column
                    $nameInput = $row.find('td:visible').first().find('input[type="text"]');
                }
                if ($nameInput.length && $nameInput.val()) {
                    autoPopulateSlug($nameInput);
                }
            });
        }, 500);
        
        // Handle dynamically added rows
        $(document).on('formset:added', function(event, $row) {
            // Hide original column in new row
            hideOriginalColumn();
            
            // Setup slug auto-populate for new row - multiple approaches
            setTimeout(function() {
                // Find name input by ID
                var $nameInput = $row.find('input[id*="-name"]');
                if (!$nameInput.length) {
                    // Fallback: find first text input
                    $nameInput = $row.find('td:visible').first().find('input[type="text"]');
                }
                
                if ($nameInput.length) {
                    // Setup handler
                    $nameInput.on('input keyup', function() {
                        autoPopulateSlug($(this));
                    });
                    
                    // Auto-populate if name already has value
                    if ($nameInput.val()) {
                        autoPopulateSlug($nameInput);
                    }
                }
            }, 300);
            
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

