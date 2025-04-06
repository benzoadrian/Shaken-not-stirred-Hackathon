# TORNIQUET Medical AI Agent

```
  _______  _____  _____  _   _  _____  _____  _   _  ______  _______ 
 |__   __||  _  ||  _  || \ | ||_   _||  _  || | | ||  ____||__   __|
    | |   | | | || |_| ||  \| |  | |  | | | || | | || |__      | |   
    | |   | | | ||    / | . ` |  | |  | | | || | | ||  __|     | |   
    | |   | |_| || |\ \ | |\  | _| |_ | |_| || |_| || |____    | |   
    |_|   |_____||_| \_\|_| \_||_____||_____| \___/ |______|   |_|   
 ----------------------------------------------------------------- 
Hi there! Welcome to TORNIQUET Medical AI Agent!
To get started, simply message us on WhatsApp with your medical needs,
and we'll connect you with the right healthcare professional.
Saving lives through intelligent healthcare!
```

## Overview
TORNIQUET is an advanced medical AI agent designed to streamline patient access to healthcare services. By leveraging WhatsApp as a communication channel and integrating with Doctolib's appointment system, TORNIQUET helps patients find and book the most appropriate medical appointments based on their specific needs.

## Features
- **WhatsApp Accessibility**: Interact with the agent through familiar messaging platform
- **Smart Appointment Booking**: Find the best available appointments based on your medical needs
- **Symptom Analysis**: Describe your pain or symptoms and get matched with appropriate specialists
- **Direct Doctor Selection**: Request appointments with specific doctors in our clinic
- **Doctolib Integration**: Seamless connection to our clinic's Doctolib scheduling system
- **Real-time Availability**: Check current appointment slots without leaving WhatsApp

## How It Works
1. Send a message to our WhatsApp number describing your medical needs:
   - Example: "I have severe lower back pain that started yesterday"
   - Example: "I need to see Dr. Martinez for a follow-up"

2. TORNIQUET will analyze your request and search available appointments on Doctolib

3. You'll receive booking options that best match your needs, with the ability to confirm directly in WhatsApp

## Getting Started
1. Save our WhatsApp number to your contacts: +XX XX XX XX XX
2. Send a message describing your medical concern or doctor preference
3. Follow the prompts to confirm your appointment

## Repository Structure
Our repository is organized into the following main directories:

- **LLM&Scraper**: Contains the language model implementation and web scraping components that power TORNIQUET's natural language understanding and Doctolib data extraction
  
- **front-end**: The user interface components for admin dashboard and monitoring tools

- **save-clinic-details**: Scripts and utilities for saving and managing clinic information in our database

- **send-whatsapp**: Services responsible for sending outgoing WhatsApp messages to users

- **whatsapp-webhook**: Webhook implementation for receiving and processing incoming WhatsApp messages from users

Each component works together to create a seamless experience from receiving patient messages to booking appropriate appointments.

## Privacy and Security
TORNIQUET prioritizes patient privacy and data security. All conversations are encrypted and medical information is handled in compliance with healthcare privacy regulations. Patient data is only used to facilitate appointment bookings and improve service quality.

## Use Cases
- **Urgent Care Needs**: Quickly find available appointments for sudden medical issues
- **Specialist Referrals**: Match symptoms with the appropriate medical specialist
- **Regular Check-ups**: Easily schedule routine appointments with your preferred doctor
- **Follow-up Visits**: Book follow-up appointments without calling the clinic
- **After-hours Requests**: Submit appointment requests anytime, even outside clinic hours

## Support
If you experience any issues with TORNIQUET or need assistance:
- **Help Command**: Send "HELP" to our WhatsApp number
- **Email Support**: [support@torniquet.ai](mailto:support@torniquet.ai)
- **Clinic Phone**: Call our front desk during business hours at +XX XX XX XX XX

## About Our Clinic
TORNIQUET is currently implemented at [Clinic Name], providing our patients with convenient access to our healthcare professionals. Our team of specialists covers multiple medical disciplines to address a wide range of health concerns.

---

TORNIQUET - Connecting Patients with Healthcare, One Message at a Time
