"""
Notification Manager - Handles email and SMS notifications for AFH properties
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any
from loguru import logger
from twilio.rest import Client
import json
from datetime import datetime

class NotificationManager:
    """Manages email and SMS notifications for AFH property alerts"""
    
    def __init__(self, notification_config: Dict[str, Any]):
        """Initialize notification manager with configuration"""
        self.config = notification_config
        self.email_config = notification_config.get('email', {})
        self.sms_config = notification_config.get('sms', {})
        
        # Initialize Twilio client for SMS
        if self.sms_config.get('enabled', False):
            try:
                self.twilio_client = Client(
                    os.getenv('TWILIO_ACCOUNT_SID'),
                    os.getenv('TWILIO_AUTH_TOKEN')
                )
                logger.info("Twilio SMS client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Twilio client: {e}")
                self.twilio_client = None
        else:
            self.twilio_client = None
    
    def send_property_alerts(self, properties: List[Dict[str, Any]]) -> bool:
        """Send alerts for new AFH properties"""
        try:
            logger.info(f"Sending alerts for {len(properties)} properties")
            
            # Send email notifications
            email_success = self._send_email_alerts(properties)
            
            # Send SMS notifications
            sms_success = self._send_sms_alerts(properties)
            
            success = email_success and sms_success
            logger.info(f"Notification sending completed. Success: {success}")
            return success
            
        except Exception as e:
            logger.error(f"Error sending property alerts: {e}")
            return False
    
    def _send_email_alerts(self, properties: List[Dict[str, Any]]) -> bool:
        """Send email alerts for properties"""
        if not self.email_config.get('enabled', False):
            logger.info("Email notifications disabled")
            return True
        
        try:
            # Create email content
            subject = f"AFH Property Alert: {len(properties)} New Properties Found"
            body = self._create_email_body(properties)
            
            # Setup email
            msg = MIMEMultipart()
            msg['From'] = os.getenv('SENDER_EMAIL')
            msg['To'] = ', '.join(self.email_config.get('recipient_emails', []))
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.email_config.get('smtp_server', 'smtp.gmail.com'), 
                                self.email_config.get('smtp_port', 587))
            server.starttls()
            server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))
            
            text = msg.as_string()
            server.sendmail(os.getenv('SENDER_EMAIL'), 
                          self.email_config.get('recipient_emails', []), text)
            server.quit()
            
            logger.info("Email alerts sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email alerts: {e}")
            return False
    
    def _send_sms_alerts(self, properties: List[Dict[str, Any]]) -> bool:
        """Send SMS alerts for properties"""
        if not self.sms_config.get('enabled', False) or not self.twilio_client:
            logger.info("SMS notifications disabled or Twilio not configured")
            return True
        
        try:
            # Create SMS content
            message_body = self._create_sms_body(properties)
            
            # Send SMS
            message = self.twilio_client.messages.create(
                body=message_body,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                to=os.getenv('RECIPIENT_PHONE')
            )
            
            logger.info(f"SMS alert sent successfully. SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending SMS alerts: {e}")
            return False
    
    def _create_email_body(self, properties: List[Dict[str, Any]]) -> str:
        """Create HTML email body for property alerts"""
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .property {{ border: 1px solid #ddd; margin: 20px 0; padding: 15px; border-radius: 5px; }}
                .property-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; }}
                .property-details {{ margin: 10px 0; }}
                .property-details span {{ margin-right: 20px; }}
                .analysis {{ background-color: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 3px; }}
                .viable {{ color: #27ae60; font-weight: bold; }}
                .not-viable {{ color: #e74c3c; font-weight: bold; }}
                .recommendations {{ background-color: #e8f4fd; padding: 10px; margin: 10px 0; border-radius: 3px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏠 AFH Property Scout Alert</h1>
                <p>Found {len(properties)} new properties matching your criteria</p>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        for i, property_data in enumerate(properties, 1):
            prop = property_data['property']
            analysis = property_data['analysis']
            
            viability_class = 'viable' if analysis['viable'] else 'not-viable'
            viability_text = 'VIABLE' if analysis['viable'] else 'NOT VIABLE'
            
            html_body += f"""
            <div class="property">
                <div class="property-title">
                    Property #{i}: {prop.get('address', 'Unknown Address')}
                </div>
                
                <div class="property-details">
                    <span><strong>Price:</strong> ${prop.get('price', 0):,.0f}</span>
                    <span><strong>Beds:</strong> {prop.get('bedrooms', 0)}</span>
                    <span><strong>Baths:</strong> {prop.get('bathrooms', 0)}</span>
                    <span><strong>Sqft:</strong> {prop.get('sqft', 0):,}</span>
                    <span><strong>County:</strong> {prop.get('county', 'Unknown')}</span>
                </div>
                
                <div class="property-details">
                    <span><strong>WABO Status:</strong> {prop.get('wabo_status', 'Unknown')}</span>
                    <span><strong>Source:</strong> {prop.get('source', 'Unknown')}</span>
                </div>
                
                <div class="analysis">
                    <p><strong>Viability Score:</strong> <span class="{viability_class}">{analysis['viability_score']:.1f}% - {viability_text}</span></p>
                    <p><strong>Monthly Cash Flow:</strong> ${analysis['financial_analysis']['monthly_cash_flow']:,.0f}</p>
                    <p><strong>Cap Rate:</strong> {analysis['financial_analysis']['cap_rate']:.2%}</p>
                    <p><strong>Optimal Price:</strong> ${analysis['pricing_analysis']['optimal_price']:,.0f}</p>
                </div>
                
                <div class="recommendations">
                    <strong>Key Recommendations:</strong>
                    <ul>
            """
            
            for rec in analysis['recommendations'][:3]:  # Show top 3 recommendations
                html_body += f"<li>{rec}</li>"
            
            html_body += """
                    </ul>
                </div>
                
                <p><strong>Property URL:</strong> <a href="{url}">{url}</a></p>
            </div>
            """.format(url=prop.get('url', 'No URL available'))
        
        html_body += """
            <div class="footer">
                <p>This alert was generated by AFH Property Scout</p>
                <p>For questions or to modify your search criteria, please contact the system administrator</p>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def _create_sms_body(self, properties: List[Dict[str, Any]]) -> str:
        """Create SMS body for property alerts"""
        if len(properties) == 1:
            prop = properties[0]['property']
            analysis = properties[0]['analysis']
            
            message = f"""🏠 AFH Property Alert!
            
{prop.get('address', 'Unknown')}
${prop.get('price', 0):,.0f} | {prop.get('bedrooms', 0)}bd/{prop.get('bathrooms', 0)}ba | {prop.get('sqft', 0):,}sqft

Viability: {analysis['viability_score']:.0f}% {'✅' if analysis['viable'] else '❌'}
Cash Flow: ${analysis['financial_analysis']['monthly_cash_flow']:,.0f}/mo
Optimal Price: ${analysis['pricing_analysis']['optimal_price']:,.0f}

{prop.get('url', '')[:50]}..."""
            
        else:
            viable_count = sum(1 for p in properties if p['analysis']['viable'])
            message = f"""🏠 AFH Property Alert!

Found {len(properties)} new properties
{viable_count} viable for AFH operation

Top property:
{properties[0]['property'].get('address', 'Unknown')[:30]}...
${properties[0]['property'].get('price', 0):,.0f} | {properties[0]['analysis']['viability_score']:.0f}% viable

Check email for full details."""
        
        return message
    
    def send_daily_summary(self, summary_data: Dict[str, Any]) -> bool:
        """Send daily summary of property search results"""
        try:
            logger.info("Sending daily summary")
            
            # Create summary content
            subject = f"AFH Property Scout - Daily Summary ({summary_data.get('date', 'Unknown')})"
            body = self._create_summary_email_body(summary_data)
            
            # Send email
            if self.email_config.get('enabled', False):
                msg = MIMEMultipart()
                msg['From'] = os.getenv('SENDER_EMAIL')
                msg['To'] = ', '.join(self.email_config.get('recipient_emails', []))
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                
                server = smtplib.SMTP(self.email_config.get('smtp_server', 'smtp.gmail.com'), 
                                    self.email_config.get('smtp_port', 587))
                server.starttls()
                server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))
                
                text = msg.as_string()
                server.sendmail(os.getenv('SENDER_EMAIL'), 
                              self.email_config.get('recipient_emails', []), text)
                server.quit()
            
            logger.info("Daily summary sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
            return False
    
    def _create_summary_email_body(self, summary_data: Dict[str, Any]) -> str:
        """Create HTML email body for daily summary"""
        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px 20px; text-align: center; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
                .metric-label {{ font-size: 14px; color: #7f8c8d; }}
                .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 AFH Property Scout - Daily Summary</h1>
                <p>{summary_data.get('date', 'Unknown Date')}</p>
            </div>
            
            <div class="summary">
                <div class="metric">
                    <div class="metric-value">{summary_data.get('total_properties', 0)}</div>
                    <div class="metric-label">Total Properties Found</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{summary_data.get('viable_properties', 0)}</div>
                    <div class="metric-label">Viable Properties</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{summary_data.get('new_properties', 0)}</div>
                    <div class="metric-label">New Properties</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{summary_data.get('sources_searched', 0)}</div>
                    <div class="metric-label">Sources Searched</div>
                </div>
            </div>
            
            <div class="footer">
                <p>AFH Property Scout - Automated Daily Search</p>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def send_error_alert(self, error_message: str, context: str = "") -> bool:
        """Send error alert to administrators"""
        try:
            subject = f"AFH Property Scout - Error Alert"
            body = f"""
            <html>
            <body>
                <h2>🚨 AFH Property Scout Error</h2>
                <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Context:</strong> {context}</p>
                <p><strong>Error:</strong></p>
                <pre>{error_message}</pre>
            </body>
            </html>
            """
            
            if self.email_config.get('enabled', False):
                msg = MIMEMultipart()
                msg['From'] = os.getenv('SENDER_EMAIL')
                msg['To'] = ', '.join(self.email_config.get('recipient_emails', []))
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                
                server = smtplib.SMTP(self.email_config.get('smtp_server', 'smtp.gmail.com'), 
                                    self.email_config.get('smtp_port', 587))
                server.starttls()
                server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))
                
                text = msg.as_string()
                server.sendmail(os.getenv('SENDER_EMAIL'), 
                              self.email_config.get('recipient_emails', []), text)
                server.quit()
            
            logger.info("Error alert sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error sending error alert: {e}")
            return False
