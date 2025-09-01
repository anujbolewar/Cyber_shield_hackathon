"""
Alert management system for social media monitoring
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

class AlertRule:
    """Represents an alert rule configuration"""
    
    def __init__(self, name: str, type: str, platforms: List[str], 
                 threshold: float, severity: str, notifications: List[str]):
        self.id = f"rule_{random.randint(1000, 9999)}"
        self.name = name
        self.type = type
        self.platforms = platforms
        self.threshold = threshold
        self.severity = severity
        self.notifications = notifications
        self.enabled = True
        self.created_at = datetime.now()
        self.trigger_count = 0
        
    def to_dict(self):
        """Convert rule to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'platforms': self.platforms,
            'threshold': self.threshold,
            'severity': self.severity,
            'notifications': self.notifications,
            'enabled': self.enabled,
            'created_at': self.created_at,
            'trigger_count': self.trigger_count
        }

class Alert:
    """Represents an active alert"""
    
    def __init__(self, rule_id: str, title: str, description: str, 
                 platform: str, metric: str, current_value: float, 
                 threshold: float, severity: str):
        self.id = f"alert_{random.randint(10000, 99999)}"
        self.rule_id = rule_id
        self.title = title
        self.description = description
        self.platform = platform
        self.metric = metric
        self.current_value = current_value
        self.threshold = threshold
        self.severity = severity
        self.status = 'Active'
        self.timestamp = datetime.now()
        self.resolved_at = None
        self.snoozed_until = None
        self.escalated = False
        self.timeline = []
        
    def resolve(self):
        """Resolve the alert"""
        self.status = 'Resolved'
        self.resolved_at = datetime.now()
        self.timeline.append({
            'timestamp': self.resolved_at,
            'event': 'Alert resolved'
        })
    
    def snooze(self, hours: int = 1):
        """Snooze the alert for specified hours"""
        self.status = 'Snoozed'
        self.snoozed_until = datetime.now() + timedelta(hours=hours)
        self.timeline.append({
            'timestamp': datetime.now(),
            'event': f'Alert snoozed for {hours} hour(s)'
        })
    
    def escalate(self):
        """Escalate the alert"""
        self.escalated = True
        self.timeline.append({
            'timestamp': datetime.now(),
            'event': 'Alert escalated'
        })
    
    def to_dict(self):
        """Convert alert to dictionary"""
        return {
            'id': self.id,
            'rule_id': self.rule_id,
            'title': self.title,
            'description': self.description,
            'platform': self.platform,
            'metric': self.metric,
            'current_value': self.current_value,
            'threshold': self.threshold,
            'severity': self.severity,
            'status': self.status,
            'timestamp': self.timestamp,
            'resolved_at': self.resolved_at,
            'snoozed_until': self.snoozed_until,
            'escalated': self.escalated,
            'timeline': self.timeline
        }

class AlertManager:
    """Manages alert rules and active alerts"""
    
    def __init__(self):
        self.rules: List[AlertRule] = []
        self.alerts: List[Alert] = []
        self.alert_history: List[Alert] = []
        self._initialize_default_rules()
        self._generate_sample_alerts()
    
    def _initialize_default_rules(self):
        """Initialize with some default alert rules"""
        default_rules = [
            {
                'name': 'High Mention Volume',
                'type': 'Mention Spike',
                'platforms': ['Twitter', 'Facebook'],
                'threshold': 100,
                'severity': 'High',
                'notifications': ['Email', 'In-App']
            },
            {
                'name': 'Negative Sentiment Alert',
                'type': 'Sentiment Drop',
                'platforms': ['Twitter', 'Instagram'],
                'threshold': -0.5,
                'severity': 'Critical',
                'notifications': ['Email', 'Slack', 'SMS']
            },
            {
                'name': 'Low Engagement Warning',
                'type': 'Engagement Drop',
                'platforms': ['Facebook', 'LinkedIn'],
                'threshold': 0.02,
                'severity': 'Medium',
                'notifications': ['In-App']
            }
        ]
        
        for rule_config in default_rules:
            rule = AlertRule(**rule_config)
            rule.trigger_count = random.randint(5, 50)
            self.rules.append(rule)
    
    def _generate_sample_alerts(self):
        """Generate some sample active alerts"""
        sample_alerts = [
            {
                'title': 'Mention Spike Detected',
                'description': 'Unusual spike in mentions detected on Twitter. Current volume is 350% above normal.',
                'platform': 'Twitter',
                'metric': 'Mentions',
                'current_value': 450,
                'threshold': 100,
                'severity': 'High'
            },
            {
                'title': 'Negative Sentiment Surge',
                'description': 'Sentiment has dropped significantly on Instagram. Immediate attention required.',
                'platform': 'Instagram',
                'metric': 'Sentiment',
                'current_value': -0.65,
                'threshold': -0.5,
                'severity': 'Critical'
            },
            {
                'title': 'Engagement Rate Drop',
                'description': 'Engagement rate on Facebook has fallen below acceptable threshold.',
                'platform': 'Facebook',
                'metric': 'Engagement Rate',
                'current_value': 0.015,
                'threshold': 0.02,
                'severity': 'Medium'
            }
        ]
        
        for alert_config in sample_alerts:
            if random.random() > 0.5:  # Only create some alerts
                alert = Alert(
                    rule_id=random.choice(self.rules).id if self.rules else 'default',
                    **alert_config
                )
                # Add some timeline events
                alert.timeline = [
                    {
                        'timestamp': alert.timestamp,
                        'event': 'Alert triggered'
                    },
                    {
                        'timestamp': alert.timestamp + timedelta(minutes=5),
                        'event': 'Notification sent'
                    }
                ]
                self.alerts.append(alert)
    
    def add_rule(self, rule: AlertRule):
        """Add a new alert rule"""
        self.rules.append(rule)
    
    def get_all_rules(self) -> List[Dict[str, Any]]:
        """Get all alert rules"""
        return [rule.to_dict() for rule in self.rules]
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        active_alerts = []
        for alert in self.alerts:
            if alert.status == 'Active' or (
                alert.status == 'Snoozed' and 
                alert.snoozed_until and 
                datetime.now() > alert.snoozed_until
            ):
                # If snoozed period has passed, reactivate
                if alert.status == 'Snoozed' and datetime.now() > alert.snoozed_until:
                    alert.status = 'Active'
                active_alerts.append(alert.to_dict())
        return active_alerts
    
    def resolve_alert(self, alert_id: str):
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolve()
                self.alert_history.append(alert)
                self.alerts.remove(alert)
                break
    
    def snooze_alert(self, alert_id: str, hours: int = 1):
        """Snooze an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.snooze(hours)
                break
    
    def escalate_alert(self, alert_id: str):
        """Escalate an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.escalate()
                # Could trigger additional notifications here
                break
    
    def silence_all_alerts(self):
        """Silence all active alerts temporarily"""
        for alert in self.alerts:
            if alert.status == 'Active':
                alert.snooze(1)  # Snooze for 1 hour
    
    def disable_rule(self, rule_id: str):
        """Disable an alert rule"""
        for rule in self.rules:
            if rule.id == rule_id:
                rule.enabled = False
                break
    
    def enable_rule(self, rule_id: str):
        """Enable an alert rule"""
        for rule in self.rules:
            if rule.id == rule_id:
                rule.enabled = True
                break
    
    def delete_rule(self, rule_id: str):
        """Delete an alert rule"""
        self.rules = [rule for rule in self.rules if rule.id != rule_id]
    
    def test_rule(self, rule_id: str):
        """Generate a test alert for a rule"""
        rule = next((r for r in self.rules if r.id == rule_id), None)
        if rule:
            test_alert = Alert(
                rule_id=rule.id,
                title=f"Test Alert - {rule.name}",
                description="This is a test alert generated manually.",
                platform=rule.platforms[0] if rule.platforms else 'Twitter',
                metric='Test Metric',
                current_value=rule.threshold + 10,
                threshold=rule.threshold,
                severity=rule.severity
            )
            self.alerts.append(test_alert)
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics for dashboard"""
        active_count = len(self.get_active_alerts())
        critical_count = len([a for a in self.alerts if a.severity == 'Critical' and a.status == 'Active'])
        
        # Calculate response time (mock data)
        avg_response_time = random.uniform(5, 30)  # minutes
        response_time_change = random.uniform(-5, 5)
        
        # Calculate resolution rate
        total_alerts = len(self.alerts) + len(self.alert_history)
        resolved_alerts = len(self.alert_history)
        resolution_rate = resolved_alerts / total_alerts if total_alerts > 0 else 0
        
        return {
            'active_alerts': active_count,
            'critical_alerts': critical_count,
            'new_alerts_today': random.randint(0, 10),
            'critical_change': random.randint(-2, 5),
            'avg_response_time': avg_response_time,
            'response_time_change': response_time_change,
            'resolution_rate': resolution_rate,
            'resolution_change': random.uniform(-0.1, 0.1)
        }
    
    def get_alerts_by_hour(self, hour: int) -> int:
        """Get number of alerts for a specific hour (mock data)"""
        # Simulate higher activity during business hours
        if 9 <= hour <= 17:
            return random.randint(5, 15)
        else:
            return random.randint(0, 5)
    
    def get_alert_type_distribution(self) -> Dict[str, int]:
        """Get distribution of alerts by type"""
        types = {}
        for alert in self.alerts + self.alert_history:
            alert_type = getattr(alert, 'type', 'Unknown')
            types[alert_type] = types.get(alert_type, 0) + 1
        
        # If no real data, return mock data
        if not types:
            types = {
                'Mention Spike': random.randint(5, 20),
                'Sentiment Drop': random.randint(3, 15),
                'Engagement Drop': random.randint(2, 10),
                'Keyword Alert': random.randint(1, 8)
            }
        
        return types
    
    def get_alert_severity_distribution(self) -> Dict[str, int]:
        """Get distribution of alerts by severity"""
        severities = {}
        for alert in self.alerts + self.alert_history:
            severity = alert.severity
            severities[severity] = severities.get(severity, 0) + 1
        
        # If no real data, return mock data
        if not severities:
            severities = {
                'Critical': random.randint(1, 5),
                'High': random.randint(3, 10),
                'Medium': random.randint(5, 15),
                'Low': random.randint(2, 8)
            }
        
        return severities
    
    def get_response_time_data(self) -> List[float]:
        """Get response time data for analysis"""
        # Generate mock response time data
        return [random.uniform(1, 60) for _ in range(50)]
    
    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history"""
        history = []
        all_alerts = sorted(
            self.alerts + self.alert_history,
            key=lambda x: x.timestamp,
            reverse=True
        )
        
        for alert in all_alerts[:limit]:
            history.append({
                'Alert ID': alert.id,
                'Title': alert.title,
                'Platform': alert.platform,
                'Severity': alert.severity,
                'Status': alert.status,
                'Triggered': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'Resolved': alert.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if alert.resolved_at else 'N/A'
            })
        
        return history

def check_alerts(df, mention_threshold: int, sentiment_threshold: float) -> List[Dict[str, Any]]:
    """Check data against alert thresholds and return triggered alerts"""
    alerts = []
    
    # Check mention threshold
    total_mentions = df['mentions'].sum() if 'mentions' in df.columns else 0
    if total_mentions > mention_threshold:
        alerts.append({
            'type': 'Mention Spike',
            'severity': 'High',
            'message': f'Mentions ({total_mentions}) exceeded threshold ({mention_threshold})',
            'value': total_mentions,
            'threshold': mention_threshold
        })
    
    # Check sentiment threshold
    avg_sentiment = df['sentiment'].mean() if 'sentiment' in df.columns else 0
    if avg_sentiment < sentiment_threshold / 100:  # Convert percentage to decimal
        alerts.append({
            'type': 'Negative Sentiment',
            'severity': 'Critical',
            'message': f'Average sentiment ({avg_sentiment:.2f}) below threshold ({sentiment_threshold/100:.2f})',
            'value': avg_sentiment,
            'threshold': sentiment_threshold / 100
        })
    
    return alerts

def display_alerts(alerts: List[Dict[str, Any]]):
    """Display alerts in Streamlit (placeholder function)"""
    # This would be implemented in the actual Streamlit app
    # Using the alert display logic from the main app
    pass
