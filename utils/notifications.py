"""
Notification system for social media monitoring alerts
"""

import smtplib
import json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Any

class NotificationManager:
    """Manages different types of notifications"""
    
    def __init__(self):
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': '',
            'password': '',
            'enabled': False
        }
        
        self.slack_config = {
            'webhook_url': '',
            'channel': '#alerts',
            'enabled': False
        }
        
        self.sms_config = {
            'api_key': '',
            'phone_numbers': [],
            'enabled': False
        }
    
    def configure_email(self, smtp_server: str, port: int, username: str, password: str):
        """Configure email notifications"""
        self.email_config.update({
            'smtp_server': smtp_server,
            'smtp_port': port,
            'username': username,
            'password': password,
            'enabled': True
        })
    
    def configure_slack(self, webhook_url: str, channel: str = '#alerts'):
        """Configure Slack notifications"""
        self.slack_config.update({
            'webhook_url': webhook_url,
            'channel': channel,
            'enabled': True
        })
    
    def configure_sms(self, api_key: str, phone_numbers: List[str]):
        """Configure SMS notifications"""
        self.sms_config.update({
            'api_key': api_key,
            'phone_numbers': phone_numbers,
            'enabled': True
        })
    
    def send_notification(self, alert_data: Dict[str, Any], notification_types: List[str]):
        """Send notification through specified channels"""
        results = {}
        
        for notification_type in notification_types:
            if notification_type == 'Email' and self.email_config['enabled']:
                results['email'] = self._send_email_notification(alert_data)
            elif notification_type == 'Slack' and self.slack_config['enabled']:
                results['slack'] = self._send_slack_notification(alert_data)
            elif notification_type == 'SMS' and self.sms_config['enabled']:
                results['sms'] = self._send_sms_notification(alert_data)
            elif notification_type == 'In-App':
                results['in_app'] = self._send_in_app_notification(alert_data)
        
        return results
    
    def _send_email_notification(self, alert_data: Dict[str, Any]) -> bool:
        """Send email notification"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['username']
            msg['To'] = 'admin@company.com'  # This would be configurable
            msg['Subject'] = f"Social Media Alert: {alert_data['title']}"
            
            # Email body
            body = self._format_email_body(alert_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['username'], 'admin@company.com', text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def _send_slack_notification(self, alert_data: Dict[str, Any]) -> bool:
        """Send Slack notification"""
        try:
            # Format Slack message
            message = self._format_slack_message(alert_data)
            
            # Send to Slack
            response = requests.post(
                self.slack_config['webhook_url'],
                data=json.dumps(message),
                headers={'Content-Type': 'application/json'}
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send Slack notification: {e}")
            return False
    
    def _send_sms_notification(self, alert_data: Dict[str, Any]) -> bool:
        """Send SMS notification"""
        try:
            # Format SMS message
            message = self._format_sms_message(alert_data)
            
            # This would integrate with SMS service (Twilio, AWS SNS, etc.)
            # For demo purposes, we'll just simulate success
            print(f"SMS would be sent: {message}")
            
            return True
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False
    
    def _send_in_app_notification(self, alert_data: Dict[str, Any]) -> bool:
        """Send in-app notification"""
        # For Streamlit, this would be handled by the UI
        # In a real application, this might use WebSocket or push notifications
        return True
    
    def _format_email_body(self, alert_data: Dict[str, Any]) -> str:
        """Format email body HTML"""
        severity_color = {
            'Critical': '#f44336',
            'High': '#ff9800',
            'Medium': '#9c27b0',
            'Low': '#4caf50'
        }.get(alert_data.get('severity', 'Medium'), '#9c27b0')
        
        html_body = f"""
        <html>
        <body>
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: {severity_color}; color: white; padding: 20px; text-align: center;">
                    <h1>Social Media Alert</h1>
                    <h2>{alert_data.get('title', 'Alert Triggered')}</h2>
                </div>
                
                <div style="padding: 20px; background-color: #f9f9f9;">
                    <h3>Alert Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Platform:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert_data.get('platform', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Severity:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert_data.get('severity', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Metric:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert_data.get('metric', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Current Value:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert_data.get('current_value', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Threshold:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{alert_data.get('threshold', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Time:</strong></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="padding: 20px; background-color: #fff;">
                    <h3>Description</h3>
                    <p>{alert_data.get('description', 'No description available.')}</p>
                </div>
                
                <div style="padding: 20px; background-color: #f0f0f0; text-align: center;">
                    <p style="margin: 0; color: #666;">
                        This alert was generated by the Social Media Monitoring System at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def _format_slack_message(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format Slack message"""
        severity_emoji = {
            'Critical': '🚨',
            'High': '⚠️',
            'Medium': '🔔',
            'Low': 'ℹ️'
        }.get(alert_data.get('severity', 'Medium'), '🔔')
        
        severity_color = {
            'Critical': 'danger',
            'High': 'warning',
            'Medium': '#9c27b0',
            'Low': 'good'
        }.get(alert_data.get('severity', 'Medium'), '#9c27b0')
        
        message = {
            "channel": self.slack_config['channel'],
            "username": "Social Media Monitor",
            "icon_emoji": ":warning:",
            "attachments": [
                {
                    "color": severity_color,
                    "title": f"{severity_emoji} {alert_data.get('title', 'Alert Triggered')}",
                    "title_link": "https://your-dashboard.com/alerts",
                    "fields": [
                        {
                            "title": "Platform",
                            "value": alert_data.get('platform', 'N/A'),
                            "short": True
                        },
                        {
                            "title": "Severity",
                            "value": alert_data.get('severity', 'N/A'),
                            "short": True
                        },
                        {
                            "title": "Metric",
                            "value": alert_data.get('metric', 'N/A'),
                            "short": True
                        },
                        {
                            "title": "Current Value",
                            "value": str(alert_data.get('current_value', 'N/A')),
                            "short": True
                        },
                        {
                            "title": "Threshold",
                            "value": str(alert_data.get('threshold', 'N/A')),
                            "short": True
                        },
                        {
                            "title": "Time",
                            "value": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            "short": True
                        }
                    ],
                    "text": alert_data.get('description', 'No description available.'),
                    "footer": "Social Media Monitor",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        }
        
        return message
    
    def _format_sms_message(self, alert_data: Dict[str, Any]) -> str:
        """Format SMS message"""
        message = f"""
🚨 SOCIAL MEDIA ALERT

{alert_data.get('title', 'Alert Triggered')}

Platform: {alert_data.get('platform', 'N/A')}
Severity: {alert_data.get('severity', 'N/A')}
Value: {alert_data.get('current_value', 'N/A')} (Threshold: {alert_data.get('threshold', 'N/A')})

Time: {datetime.now().strftime('%H:%M %d/%m/%Y')}

Check dashboard for details.
        """.strip()
        
        return message

def send_notification(alert_data: Dict[str, Any], notification_types: List[str]):
    """Convenience function to send notifications"""
    notification_manager = NotificationManager()
    return notification_manager.send_notification(alert_data, notification_types)

def send_test_notification(notification_type: str):
    """Send a test notification"""
    test_alert = {
        'title': 'Test Alert - System Check',
        'description': 'This is a test notification to verify the alert system is working correctly.',
        'platform': 'System',
        'severity': 'Low',
        'metric': 'Test Metric',
        'current_value': 100,
        'threshold': 50
    }
    
    notification_manager = NotificationManager()
    return notification_manager.send_notification(test_alert, [notification_type])

def format_alert_summary(alerts: List[Dict[str, Any]]) -> str:
    """Format a summary of multiple alerts"""
    if not alerts:
        return "No active alerts."
    
    summary = f"Alert Summary ({len(alerts)} active alerts):\n\n"
    
    for i, alert in enumerate(alerts[:5], 1):  # Show up to 5 alerts
        summary += f"{i}. {alert.get('title', 'Unknown Alert')}\n"
        summary += f"   Platform: {alert.get('platform', 'N/A')} | Severity: {alert.get('severity', 'N/A')}\n"
        summary += f"   Value: {alert.get('current_value', 'N/A')} (Threshold: {alert.get('threshold', 'N/A')})\n\n"
    
    if len(alerts) > 5:
        summary += f"... and {len(alerts) - 5} more alerts.\n"
    
    return summary

def send_daily_summary(alerts: List[Dict[str, Any]], metrics: Dict[str, Any]):
    """Send daily summary notification"""
    summary_data = {
        'title': 'Daily Social Media Summary',
        'description': format_daily_summary(alerts, metrics),
        'platform': 'System',
        'severity': 'Low',
        'metric': 'Daily Summary',
        'current_value': len(alerts),
        'threshold': 0
    }
    
    notification_manager = NotificationManager()
    return notification_manager.send_notification(summary_data, ['Email'])

def format_daily_summary(alerts: List[Dict[str, Any]], metrics: Dict[str, Any]) -> str:
    """Format daily summary content"""
    summary = f"""
Daily Social Media Monitoring Summary - {datetime.now().strftime('%Y-%m-%d')}

ALERTS:
- Total Active Alerts: {len(alerts)}
- Critical Alerts: {len([a for a in alerts if a.get('severity') == 'Critical'])}
- High Priority Alerts: {len([a for a in alerts if a.get('severity') == 'High'])}

METRICS:
- Total Mentions: {metrics.get('total_mentions', 'N/A')}
- Average Sentiment: {metrics.get('avg_sentiment', 'N/A'):.2f}
- Engagement Rate: {metrics.get('engagement_rate', 'N/A'):.2%}
- Total Reach: {metrics.get('total_reach', 'N/A'):,}

TOP PLATFORMS:
1. Twitter - {metrics.get('twitter_mentions', 'N/A')} mentions
2. Facebook - {metrics.get('facebook_mentions', 'N/A')} mentions
3. Instagram - {metrics.get('instagram_mentions', 'N/A')} mentions

RECOMMENDATIONS:
- Monitor critical alerts closely
- Consider increasing engagement on underperforming platforms
- Review negative sentiment sources

This summary was generated automatically by the Social Media Monitoring System.
    """.strip()
    
    return summary
