// Category Mega Menu JavaScript - Same behavior as Shop Menu
(function($) {
    $(document).ready(function() {
        // Handle mega menu hover - same as shop menu
        $('.category-menu > li.has-mega-menu').on('mouseenter', function() {
            var $megaMenu = $(this).find('.category-mega-menu');
            var $li = $(this);
            
            // Calculate position to ensure it doesn't go off screen
            var windowWidth = $(window).width();
            var liOffset = $li.offset();
            var liWidth = $li.outerWidth();
            var megaMenuWidth = $megaMenu.outerWidth();
            var megaMenuLeft = liOffset.left + liWidth + 5;
            
            // If mega menu would go off screen, position it to the left
            if (megaMenuLeft + megaMenuWidth > windowWidth) {
                $megaMenu.css({
                    'left': 'auto',
                    'right': '100%',
                    'margin-left': '0',
                    'margin-right': '5px'
                });
            } else {
                $megaMenu.css({
                    'left': '100%',
                    'right': 'auto',
                    'margin-left': '5px',
                    'margin-right': '0'
                });
            }
        });
        
        // Handle window resize
        $(window).on('resize', function() {
            $('.category-menu > li.has-mega-menu').each(function() {
                var $megaMenu = $(this).find('.category-mega-menu');
                if ($megaMenu.css('opacity') === '1' || $megaMenu.css('visibility') === 'visible') {
                    var $li = $(this);
                    var windowWidth = $(window).width();
                    var liOffset = $li.offset();
                    var liWidth = $li.outerWidth();
                    var megaMenuWidth = $megaMenu.outerWidth();
                    var megaMenuLeft = liOffset.left + liWidth + 5;
                    
                    if (megaMenuLeft + megaMenuWidth > windowWidth) {
                        $megaMenu.css({
                            'left': 'auto',
                            'right': '100%',
                            'margin-left': '0',
                            'margin-right': '5px'
                        });
                    } else {
                        $megaMenu.css({
                            'left': '100%',
                            'right': 'auto',
                            'margin-left': '5px',
                            'margin-right': '0'
                        });
                    }
                }
            });
        });
    });
})(django.jQuery || jQuery);

