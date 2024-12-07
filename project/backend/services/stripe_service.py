import stripe
from flask import current_app

stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

class StripeService:
    @staticmethod
    def create_checkout_session(user_id, price_id):
        try:
            user = User.query.get(user_id)
            session = stripe.checkout.Session.create(
                customer=user.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription',
                success_url='http://yourapp.com/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://yourapp.com/cancel',
            )
            return session
        except Exception as e:
            current_app.logger.error(f"Stripe error: {str(e)}")
            raise