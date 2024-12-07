const stripe = Stripe('your_publishable_key');

async function handleSubscription() {
    try {
        const response = await fetch('/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                priceId: 'your_price_id'
            })
        });
        
        const session = await response.json();
        
        // Redirect to Stripe Checkout
        const result = await stripe.redirectToCheckout({
            sessionId: session.sessionId
        });
        
        if (result.error) {
            showToast(result.error.message, 'error');
        }
    } catch (error) {
        showToast('Payment failed', 'error');
        console.error('Error:', error);
    }
}