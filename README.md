# SACCO SMS Manager

A Frappe application for managing SACCO (Saving and Credit Organization) members and sending SMS notifications for membership fees, saving/loan payments, and announcements.

## Features

- **Member Management**: Comprehensive member profiles with personal, family, professional, education, and address information
- **Group SMS Messaging**: Create campaigns to send SMS to selected members or all members
- **Membership Fee Reminders**: Automatic SMS reminders 3 days before, on due date, and 3 days after
- **Loan/Saving Payment Reminders**: Daily automated reminders for due payments
- **SMS Gateway Integration**: Configurable SMS provider (API URL, key, sender ID)
- **Dashboard**: Overview of members, pending payments, and SMS stats
- **REST API**: Endpoints for SMS sending and dashboard data

## Installation

### Prerequisites

- Frappe Framework (v16+)
- Bench

### Steps

1. **Get the app**
   ```bash
   cd frappe-bench
   bench get-app sacco_sms_manager
   # Or if developing locally:
   # bench get-app /path/to/sacco_sms_manager
   ```

2. **Install on a site**
   ```bash
   bench --site your-site.local install-app sacco_sms_manager
   ```

3. **Configure SMS Settings**
   - Go to **SACCO** workspace → **SMS Settings**
   - Enter your SMS provider's API URL, API Key, and Sender ID
   - Mark as Active when ready

4. **Ensure scheduler is running** (for automated reminders)
   ```bash
   bench enable-scheduler
   bench start
   ```

## Usage

### Member Management

- Create members via **SACCO** → **Members**
- Use "Send SMS" button on member form for quick messages
- Use "Send Bulk SMS" from member list (select rows first)

### SMS Campaigns

- Create campaigns with message and target members
- Option: "Send to All Members" for broadcasts
- Use "Send Now" or schedule for later
- Scheduled campaigns are processed hourly

### Payment Reminders

- Create **Membership Fee Payment** and **Loan Saving Payment** records
- Automatic reminders run daily (3 days before, on due date, 3 days after for membership)
- Use "Send Reminder SMS" button for manual trigger

### REST API

- `POST /api/method/sacco_sms_manager.api.send_sms_to_member` – Send SMS to one member
- `POST /api/method/sacco_sms_manager.api.send_bulk_sms` – Send SMS to multiple members
- `POST /api/method/sacco_sms_manager.api.send_campaign_now` – Trigger campaign
- `GET /api/method/sacco_sms_manager.api.get_dashboard_stats` – Dashboard statistics

## Roles & Permissions

| Role          | Access                                              |
|---------------|-----------------------------------------------------|
| SACCO Admin   | Full access to all DocTypes and settings            |
| SACCO Officer | Manage members, send SMS, create campaigns          |
| Accountant    | Manage membership and loan/saving payments, reminders |

## SMS Gateway

The app uses a generic REST API. Configure in **SMS Settings** with:

- **API URL**: Provider endpoint (e.g. `https://api.example.com/sms/send`)
- **API Key**: Authentication
- **Sender ID**: Displayed sender

Adapt `_call_sms_gateway` in `sms_service.py` for your provider's request format (e.g. Africa's Talking, Twilio).

## Running Tests

```bash
bench --site your-site.local run-tests sacco_sms_manager
```

Or run a specific test file:

```bash
bench --site your-site.local run-tests sacco_sms_manager.sacco_sms_manager.test_member
```

## License

MIT
