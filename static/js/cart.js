// AJAX Cart Functionality
(function() {
    'use strict';
    
    console.log('Cart.js loaded');

    // Function to update cart count in header
    function updateCartCount(count) {
        const cartDots = document.querySelectorAll('.cart-dot, .icon-dot');
        cartDots.forEach(function(dot) {
            if (dot.closest('.cart-icon')) {
                dot.textContent = count;
            }
        });
    }

    // Function to show notification message
    function showNotification(message, type) {
        // Remove existing notifications
        const existing = document.querySelector('.cart-notification');
        if (existing) {
            existing.remove();
        }

        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'cart-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#9370DB' : '#dc3545'};
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 9999;
            font-size: 14px;
            font-weight: 500;
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;
        notification.textContent = message;

        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        if (!document.querySelector('#cart-notification-style')) {
            style.id = 'cart-notification-style';
            document.head.appendChild(style);
        }

        document.body.appendChild(notification);

        // Auto remove after 3 seconds
        setTimeout(function() {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(function() {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Get CSRF token from cookie or hidden input
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        // Fallback: try to get from hidden input
        if (!cookieValue) {
            const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
            if (csrfInput) {
                cookieValue = csrfInput.value;
            }
        }
        return cookieValue;
    }

    // Handle Add to Cart with AJAX
    function processAddToCart(link) {
        const url = link.getAttribute('href');
        
        console.log('Processing cart add:', url);
        
        const productCard = link.closest('.product-card, .product-item, .rts-product-item, .product-bottom-action');
        
        // Get quantity if available (from product details page)
        let quantity = 1;
        let quantityInput = null;
        
        // Try to find quantity input in the same product card or in product details page
        if (productCard) {
            quantityInput = productCard.querySelector('.quantity-edit .input, .input[type="number"], input[type="text"].input');
        }
        // If not found, try global search (for product details page)
        if (!quantityInput) {
            quantityInput = document.querySelector('.product-bottom-action .quantity-edit .input, .product-bottom-action input[type="number"], .product-bottom-action input[type="text"].input');
        }
        if (quantityInput) {
            quantity = parseInt(quantityInput.value) || 1;
        }

        // Disable button during request
        const originalText = link.innerHTML;
        link.style.opacity = '0.6';
        link.style.pointerEvents = 'none';
        const originalHref = link.getAttribute('href');
        link.setAttribute('href', 'javascript:void(0)');
        if (link.textContent) {
            link.textContent = 'Adding...';
        }

        // Make AJAX request
        fetch(originalHref, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: 'quantity=' + quantity
        })
        .then(function(response) {
            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                // If not JSON, might be a redirect or error
                throw new Error('Invalid response format');
            }
        })
        .then(function(data) {
            if (data && data.success) {
                // Update cart count
                if (data.cart_count !== undefined) {
                    updateCartCount(data.cart_count);
                }
                
                // Show success message
                showNotification(data.message || 'Product added to cart successfully!', 'success');
                
                // Add visual feedback to product card
                if (productCard) {
                    productCard.style.transition = 'all 0.3s ease';
                    productCard.style.transform = 'scale(1.05)';
                    productCard.style.boxShadow = '0 0 15px rgba(136, 51, 184, 0.5)';
                    setTimeout(function() {
                        productCard.style.transform = 'scale(1)';
                        productCard.style.boxShadow = '';
                    }, 500);
                }
            } else {
                // Show error message
                showNotification(data.message || 'Failed to add product to cart.', 'error');
            }
        })
        .catch(function(error) {
            console.error('Cart Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        })
        .finally(function() {
            // Re-enable button
            link.style.opacity = '1';
            link.style.pointerEvents = 'auto';
            link.setAttribute('href', originalHref);
            link.innerHTML = originalText;
        });
    }

    // Document-level click handler using event delegation
    function handleDocumentClick(event) {
        const target = event.target;
        // Check if clicked element or its parent is a cart link
        const link = target.closest('a[href*="add-to-cart"], a[href*="add_to_cart"], a.btn-add-to-cart, a.addto-cart, a.addto-cart-btn');
        
        if (link) {
            const url = link.getAttribute('href');
            if (url && (url.includes('add-to-cart') || url.includes('add_to_cart'))) {
                // Prevent default and handle with AJAX
                event.preventDefault();
                event.stopPropagation();
                event.stopImmediatePropagation();
                processAddToCart(link);
                return false;
            }
        }
    }

    // Setup event delegation
    function setupEventDelegation() {
        // Remove any existing listener
        if (document.body) {
            document.body.removeEventListener('click', handleDocumentClick, true);
            // Add new listener in capture phase to catch before other handlers
            document.body.addEventListener('click', handleDocumentClick, true);
            console.log('Event delegation set up for cart links');
        }
    }

    // Handle quantity buttons on product details page
    function setupQuantityButtons() {
        document.querySelectorAll('.product-bottom-action .quantity-edit, .quantity-edit').forEach(function(container) {
            const quantityMinus = container.querySelector('.minus, .button.minus');
            const quantityPlus = container.querySelector('.plus, .button.plus');
            const quantityInput = container.querySelector('.input, input[type="number"]');

            if (quantityMinus && quantityInput) {
                quantityMinus.addEventListener('click', function(e) {
                    e.preventDefault();
                    let value = parseInt(quantityInput.value) || 1;
                    if (value > 1) {
                        value--;
                        quantityInput.value = value;
                    }
                });
            }

            if (quantityPlus && quantityInput) {
                quantityPlus.addEventListener('click', function(e) {
                    e.preventDefault();
                    let value = parseInt(quantityInput.value) || 1;
                    const maxStock = parseInt(quantityInput.getAttribute('max')) || 999;
                    if (value < maxStock) {
                        value++;
                        quantityInput.value = value;
                    } else {
                        showNotification('Maximum stock available: ' + maxStock, 'error');
                    }
                });
            }
        });
    }

    // Initialize on page load
    function initialize() {
        setupEventDelegation();
        setupQuantityButtons();
    }

    // Run immediately and also on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        // DOM already loaded
        initialize();
    }
    
    // Also run after a short delay to catch any late-loading content
    setTimeout(initialize, 500);

    // Re-initialize for dynamically loaded content
    const observer = new MutationObserver(function(mutations) {
        let shouldReinit = false;
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    // Check if this node or its children contain cart links
                    if (node.matches && (node.matches('a[href*="add-to-cart"], a[href*="add_to_cart"], a.btn-add-to-cart, a.addto-cart, a.addto-cart-btn') || 
                        node.querySelector && node.querySelector('a[href*="add-to-cart"], a[href*="add_to_cart"], a.btn-add-to-cart, a.addto-cart, a.addto-cart-btn'))) {
                        shouldReinit = true;
                    }
                }
            });
        });
        if (shouldReinit) {
            // Small delay to ensure DOM is ready
            setTimeout(setupEventDelegation, 100);
        }
    });

    // Start observing
    if (document.body) {
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
})();
