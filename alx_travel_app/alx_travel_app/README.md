Seeding for travel app
## Payment Integration with Chapa

This app integrates Chapa for secure payment processing.

### Features
- Initiate payments via Chapa API
- Verify transactions and update status
- Monitor payments via Django admin

### 📸 Screenshots

#### Payment Initiation
![Payment Initiation Log](screenshots/payment_initiation_log.png)

#### Payment Verification
![Payment Verification Log](screenshots/payment_verification_log.png)

#### Admin Panel Entry
![Payment Admin Entry](screenshots/payment_admin_entry.png)

###  Key Files
- `listings/models.py`: Defines the `Payment` model
- `listings/views.py`: Handles payment verification
- `listings/admin.py`: Enables admin monitoring

###  Logging
Logs are stored in `payment.log` and include:
- Initiation timestamp
- Verification status
- Errors (if any)

###  Testing
Use Django admin to confirm:
- Payment status updates correctly
- Transaction IDs are unique