// Product Variation Admin JavaScript - for standalone admin page
(function($) {
    'use strict';
    
    // Wait for both jQuery and document ready
    $(document).ready(function() {
        // Function to convert text to slug (matches Django's slugify behavior)
        function slugify(text) {
            if (!text) return '';
            return text.toString().toLowerCase()
                .trim()
                .replace(/\s+/g, '-')           // Replace spaces with -
                .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
                .replace(/\-\-+/g, '-')         // Replace multiple - with single -
                .replace(/^-+/, '')             // Trim - from start of text
                .replace(/-+$/, '');            // Trim - from end of text
        }
        
        // Function to update slug from name
        function updateSlug() {
            var $nameField = $('#id_name');
            var $slugField = $('#id_slug');
            
            if ($nameField.length && $slugField.length) {
                var nameValue = $nameField.val();
                if (nameValue && nameValue.trim()) {
                    var slugValue = slugify(nameValue);
                    // Only update if slug is empty or matches the old name-based slug
                    var currentSlug = $slugField.val();
                    if (!currentSlug || currentSlug.trim() === '' || currentSlug === slugify($nameField.data('old-value') || '')) {
                        $slugField.val(slugValue);
                    }
                } else if (!$slugField.val()) {
                    $slugField.val('');
                }
            }
        }
        
        // Find name and slug fields
        var $nameField = $('#id_name');
        var $slugField = $('#id_slug');
        
        if ($nameField.length && $slugField.length) {
            // Store initial name value
            $nameField.data('old-value', $nameField.val());
            
            // Auto-populate on input/keyup/blur
            $nameField.on('input keyup blur change', function() {
                updateSlug();
                // Update stored old value
                $nameField.data('old-value', $(this).val());
            });
            
            // Auto-populate on page load if name exists but slug is empty
            setTimeout(function() {
                if ($nameField.val() && (!$slugField.val() || $slugField.val().trim() === '')) {
                    updateSlug();
                }
            }, 100);
            
            // Also handle form submission to ensure slug is set
            $('form').on('submit', function(e) {
                var nameVal = $nameField.val();
                var slugVal = $slugField.val();
                
                // If name exists but slug is empty, generate it
                if (nameVal && nameVal.trim() && (!slugVal || slugVal.trim() === '')) {
                    $slugField.val(slugify(nameVal));
                }
            });
        } else {
            // Debug: log if fields not found
            console.warn('ProductVariation admin: Name or slug field not found');
        }
    });
})(django.jQuery || jQuery);

