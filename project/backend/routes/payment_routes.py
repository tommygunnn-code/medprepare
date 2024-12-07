from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..services.stripe_service import StripeService

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    try:
        price_id = request.json.get('priceId')
        session = StripeService.create_checkout_session(
            current_user.id, 
            price_id
        )
        return jsonify({'sessionId': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_WEBHOOK_SECRET']
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Handle successful payment
        fulfill_order(session)

    return jsonify({'status': 'success'})