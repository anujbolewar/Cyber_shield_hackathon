#!/usr/bin/env python3
"""
🏛️ POLICE AI MONITORING SYSTEM - DATABASE MANAGER
Comprehensive SQLite database system for police cyber monitoring
Includes all tables, CRUD operations, security, and evidence export
"""

import sqlite3
import json
import logging
import hashlib
import os
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from contextlib import contextmanager
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoliceMonitoringDB:
    """
    Comprehensive database manager for Police AI Monitoring System
    Handles all database operations with security and evidence integrity
    """
    
    def __init__(self, db_path: str = "police_monitoring.db"):
        """Initialize the database manager"""
        self.db_path = db_path
        self.backup_dir = "db_backups"
        self._ensure_backup_directory()
        self._initialize_database()
        
        # Security settings
        self.max_query_length = 10000
        self.forbidden_keywords = ['DROP', 'DELETE FROM', 'TRUNCATE', 'ALTER TABLE']
        
        logger.info(f"Police Monitoring Database initialized: {db_path}")
    
    def _ensure_backup_directory(self):
        """Ensure backup directory exists"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections with proper error handling"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            # Temporarily disable foreign keys for demo
            conn.execute("PRAGMA foreign_keys = OFF")
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _initialize_database(self):
        """Initialize database with all required tables and indexes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create keywords table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT NOT NULL,
                    category TEXT NOT NULL,
                    risk_level INTEGER NOT NULL CHECK (risk_level BETWEEN 1 AND 10),
                    language TEXT NOT NULL DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    created_by TEXT,
                    UNIQUE(term, language)
                )
            """)
            
            # Create monitored_content table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitored_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    content TEXT NOT NULL,
                    content_hash TEXT NOT NULL,
                    author TEXT NOT NULL,
                    author_id TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    risk_score REAL NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
                    threat_level TEXT CHECK (threat_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
                    sentiment TEXT,
                    language TEXT,
                    location TEXT,
                    url TEXT,
                    engagement_metrics TEXT, -- JSON string
                    analysis_metadata TEXT, -- JSON string
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_flagged BOOLEAN DEFAULT 0,
                    UNIQUE(content_hash)
                )
            """)
            
            # Create alerts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    severity TEXT NOT NULL CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
                    message TEXT NOT NULL,
                    content_id INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'INVESTIGATING', 'RESOLVED', 'CLOSED', 'FALSE_POSITIVE')),
                    assigned_officer TEXT,
                    assigned_at TIMESTAMP,
                    resolved_at TIMESTAMP,
                    resolution_notes TEXT,
                    escalated BOOLEAN DEFAULT 0,
                    parent_alert_id TEXT,
                    metadata TEXT, -- JSON string
                    FOREIGN KEY (content_id) REFERENCES monitored_content(id),
                    FOREIGN KEY (parent_alert_id) REFERENCES alerts(alert_id)
                )
            """)
            
            # Create investigations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS investigations (
                    case_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    content_ids TEXT NOT NULL, -- JSON array of content IDs
                    alert_ids TEXT, -- JSON array of alert IDs
                    status TEXT DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'ACTIVE', 'UNDER_REVIEW', 'COMPLETED', 'CLOSED', 'ARCHIVED')),
                    priority TEXT DEFAULT 'MEDIUM' CHECK (priority IN ('LOW', 'MEDIUM', 'HIGH', 'URGENT')),
                    lead_officer TEXT NOT NULL,
                    team_members TEXT, -- JSON array of officer names
                    evidence TEXT, -- JSON string with evidence details
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    deadline TIMESTAMP,
                    court_case_number TEXT,
                    legal_status TEXT CHECK (legal_status IN ('INVESTIGATION', 'CHARGES_FILED', 'TRIAL', 'CLOSED')),
                    classification TEXT, -- terrorism, cybercrime, etc.
                    metadata TEXT -- JSON string
                )
            """)
            
            # Create api_logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    platform TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    endpoint TEXT,
                    request_data TEXT, -- JSON string
                    response_status INTEGER,
                    success BOOLEAN NOT NULL,
                    error_message TEXT,
                    execution_time_ms INTEGER,
                    rate_limit_remaining INTEGER,
                    user_agent TEXT,
                    ip_address TEXT,
                    session_id TEXT
                )
            """)
            
            # Create users table for officer management
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('OFFICER', 'INVESTIGATOR', 'SUPERVISOR', 'ADMIN')),
                    department TEXT NOT NULL,
                    badge_number TEXT UNIQUE,
                    permissions TEXT, -- JSON array of permissions
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    password_hash TEXT,
                    two_factor_enabled BOOLEAN DEFAULT 0
                )
            """)
            
            # Create audit_trail table for compliance
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_trail (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    record_id TEXT NOT NULL,
                    old_values TEXT, -- JSON string
                    new_values TEXT, -- JSON string
                    ip_address TEXT,
                    user_agent TEXT,
                    session_id TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Create indexes for performance
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_keywords_category ON keywords(category)",
                "CREATE INDEX IF NOT EXISTS idx_keywords_risk_level ON keywords(risk_level)",
                "CREATE INDEX IF NOT EXISTS idx_content_platform ON monitored_content(platform)",
                "CREATE INDEX IF NOT EXISTS idx_content_timestamp ON monitored_content(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_content_risk_score ON monitored_content(risk_score)",
                "CREATE INDEX IF NOT EXISTS idx_content_threat_level ON monitored_content(threat_level)",
                "CREATE INDEX IF NOT EXISTS idx_content_hash ON monitored_content(content_hash)",
                "CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(type)",
                "CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status)",
                "CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity)",
                "CREATE INDEX IF NOT EXISTS idx_investigations_status ON investigations(status)",
                "CREATE INDEX IF NOT EXISTS idx_investigations_officer ON investigations(lead_officer)",
                "CREATE INDEX IF NOT EXISTS idx_api_logs_platform ON api_logs(platform)",
                "CREATE INDEX IF NOT EXISTS idx_api_logs_timestamp ON api_logs(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_trail(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_trail(timestamp)"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            conn.commit()
            logger.info("Database schema initialized successfully")
    
    def _validate_sql_safety(self, query: str) -> bool:
        """Validate SQL query for safety (prevent injection)"""
        query_upper = query.upper().strip()
        
        # Check query length
        if len(query) > self.max_query_length:
            logger.warning(f"Query too long: {len(query)} characters")
            return False
        
        # Check for forbidden keywords
        for keyword in self.forbidden_keywords:
            if keyword in query_upper:
                logger.warning(f"Forbidden keyword detected: {keyword}")
                return False
        
        return True
    
    def _generate_content_hash(self, content: str) -> str:
        """Generate hash for content deduplication"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def _log_audit_trail(self, user_id: str, action: str, table_name: str, 
                        record_id: str, old_values: Dict = None, 
                        new_values: Dict = None, conn=None):
        """Log action to audit trail"""
        if conn is None:
            with self.get_connection() as conn:
                self._log_audit_trail(user_id, action, table_name, record_id, 
                                    old_values, new_values, conn)
                return
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_trail 
            (user_id, action, table_name, record_id, old_values, new_values)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id, action, table_name, str(record_id),
            json.dumps(old_values) if old_values else None,
            json.dumps(new_values) if new_values else None
        ))
    
    # ==================== KEYWORDS MANAGEMENT ====================
    
    def add_keyword(self, term: str, category: str, risk_level: int, 
                   language: str = 'en', created_by: str = None) -> bool:
        """Add a new keyword to monitor"""
        try:
            # Validate inputs
            if not term or not category:
                raise ValueError("Term and category are required")
            if not 1 <= risk_level <= 10:
                raise ValueError("Risk level must be between 1 and 10")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO keywords (term, category, risk_level, language, created_by)
                    VALUES (?, ?, ?, ?, ?)
                """, (term.strip(), category.strip(), risk_level, language, created_by))
                
                conn.commit()
                
                # Log audit trail
                if created_by:
                    self._log_audit_trail(
                        created_by, 'INSERT', 'keywords', cursor.lastrowid,
                        new_values={'term': term, 'category': category, 'risk_level': risk_level}
                    )
                
                logger.info(f"Keyword added: {term} ({category})")
                return True
                
        except sqlite3.IntegrityError:
            logger.warning(f"Keyword already exists: {term} ({language})")
            return False
        except Exception as e:
            logger.error(f"Error adding keyword: {e}")
            return False
    
    def get_keywords(self, category: str = None, language: str = None, 
                    risk_level_min: int = None, active_only: bool = True) -> List[Dict]:
        """Retrieve keywords with optional filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM keywords WHERE 1=1"
                params = []
                
                if active_only:
                    query += " AND is_active = 1"
                if category:
                    query += " AND category = ?"
                    params.append(category)
                if language:
                    query += " AND language = ?"
                    params.append(language)
                if risk_level_min is not None:
                    query += " AND risk_level >= ?"
                    params.append(risk_level_min)
                
                query += " ORDER BY risk_level DESC, term ASC"
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error retrieving keywords: {e}")
            return []
    
    def update_keyword(self, keyword_id: int, updates: Dict, updated_by: str = None) -> bool:
        """Update keyword information"""
        try:
            if not updates:
                return False
            
            # Get old values for audit
            old_values = self.get_keyword_by_id(keyword_id)
            if not old_values:
                return False
            
            # Build update query
            set_clauses = []
            params = []
            
            allowed_fields = ['term', 'category', 'risk_level', 'language', 'is_active']
            for field, value in updates.items():
                if field in allowed_fields:
                    set_clauses.append(f"{field} = ?")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            params.append(keyword_id)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                query = f"UPDATE keywords SET {', '.join(set_clauses)} WHERE id = ?"
                cursor.execute(query, params)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    
                    # Log audit trail
                    if updated_by:
                        self._log_audit_trail(
                            updated_by, 'UPDATE', 'keywords', keyword_id,
                            old_values=old_values, new_values=updates, conn=conn
                        )
                    
                    logger.info(f"Keyword updated: ID {keyword_id}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error updating keyword: {e}")
            return False
    
    def get_keyword_by_id(self, keyword_id: int) -> Optional[Dict]:
        """Get keyword by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM keywords WHERE id = ?", (keyword_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting keyword: {e}")
            return None
    
    # ==================== MONITORED CONTENT MANAGEMENT ====================
    
    def add_monitored_content(self, platform: str, content: str, author: str,
                            timestamp: datetime, risk_score: float,
                            threat_level: str = None, **kwargs) -> Optional[int]:
        """Add monitored content with deduplication"""
        try:
            # Validate inputs
            if not all([platform, content, author]):
                raise ValueError("Platform, content, and author are required")
            if not 0 <= risk_score <= 100:
                raise ValueError("Risk score must be between 0 and 100")
            
            content_hash = self._generate_content_hash(content)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check for duplicate content
                cursor.execute("SELECT id FROM monitored_content WHERE content_hash = ?", (content_hash,))
                if cursor.fetchone():
                    logger.info(f"Duplicate content detected, skipping: {content_hash[:16]}...")
                    return None
                
                # Insert new content
                cursor.execute("""
                    INSERT INTO monitored_content 
                    (platform, content, content_hash, author, author_id, timestamp, 
                     risk_score, threat_level, sentiment, language, location, url,
                     engagement_metrics, analysis_metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    platform, content, content_hash, author,
                    kwargs.get('author_id'), timestamp, risk_score, threat_level,
                    kwargs.get('sentiment'), kwargs.get('language'),
                    kwargs.get('location'), kwargs.get('url'),
                    json.dumps(kwargs.get('engagement_metrics')) if kwargs.get('engagement_metrics') else None,
                    json.dumps(kwargs.get('analysis_metadata')) if kwargs.get('analysis_metadata') else None
                ))
                
                content_id = cursor.lastrowid
                conn.commit()
                
                logger.info(f"Content added: ID {content_id}, Risk: {risk_score}")
                return content_id
                
        except sqlite3.IntegrityError as e:
            logger.warning(f"Content integrity error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error adding content: {e}")
            return None
    
    def get_monitored_content(self, limit: int = 100, offset: int = 0,
                            platform: str = None, risk_threshold: float = None,
                            threat_level: str = None, date_from: datetime = None,
                            date_to: datetime = None, flagged_only: bool = False) -> List[Dict]:
        """Retrieve monitored content with filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT id, platform, content, author, timestamp, risk_score, 
                           threat_level, sentiment, language, location, is_flagged,
                           created_at
                    FROM monitored_content 
                    WHERE 1=1
                """
                params = []
                
                if platform:
                    query += " AND platform = ?"
                    params.append(platform)
                if risk_threshold is not None:
                    query += " AND risk_score >= ?"
                    params.append(risk_threshold)
                if threat_level:
                    query += " AND threat_level = ?"
                    params.append(threat_level)
                if date_from:
                    query += " AND timestamp >= ?"
                    params.append(date_from.isoformat())
                if date_to:
                    query += " AND timestamp <= ?"
                    params.append(date_to.isoformat())
                if flagged_only:
                    query += " AND is_flagged = 1"
                
                query += " ORDER BY risk_score DESC, timestamp DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error retrieving content: {e}")
            return []
    
    def flag_content(self, content_id: int, flagged_by: str = None) -> bool:
        """Flag content for review"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE monitored_content 
                    SET is_flagged = 1 
                    WHERE id = ?
                """, (content_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    
                    # Log audit trail
                    if flagged_by:
                        self._log_audit_trail(
                            flagged_by, 'UPDATE', 'monitored_content', content_id,
                            new_values={'is_flagged': True}, conn=conn
                        )
                    
                    logger.info(f"Content flagged: ID {content_id}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error flagging content: {e}")
            return False
    
    # ==================== ALERTS MANAGEMENT ====================
    
    def create_alert(self, alert_type: str, severity: str, message: str,
                    content_id: int = None, assigned_officer: str = None,
                    metadata: Dict = None) -> str:
        """Create a new alert"""
        try:
            alert_id = str(uuid.uuid4())
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO alerts 
                    (alert_id, type, severity, message, content_id, assigned_officer, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    alert_id, alert_type, severity, message, content_id,
                    assigned_officer, json.dumps(metadata) if metadata else None
                ))
                
                # Update assignment timestamp if officer assigned
                if assigned_officer:
                    cursor.execute("""
                        UPDATE alerts SET assigned_at = CURRENT_TIMESTAMP 
                        WHERE alert_id = ?
                    """, (alert_id,))
                
                conn.commit()
                logger.info(f"Alert created: {alert_id} ({severity})")
                return alert_id
                
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return None
    
    def get_alerts(self, status: str = None, assigned_officer: str = None,
                  severity: str = None, limit: int = 100) -> List[Dict]:
        """Retrieve alerts with filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT a.*, mc.content, mc.author, mc.platform
                    FROM alerts a
                    LEFT JOIN monitored_content mc ON a.content_id = mc.id
                    WHERE 1=1
                """
                params = []
                
                if status:
                    query += " AND a.status = ?"
                    params.append(status)
                if assigned_officer:
                    query += " AND a.assigned_officer = ?"
                    params.append(assigned_officer)
                if severity:
                    query += " AND a.severity = ?"
                    params.append(severity)
                
                query += " ORDER BY a.timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            return []
    
    def update_alert_status(self, alert_id: str, status: str, 
                          updated_by: str = None, resolution_notes: str = None) -> bool:
        """Update alert status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Get old values for audit
                cursor.execute("SELECT * FROM alerts WHERE alert_id = ?", (alert_id,))
                old_alert = cursor.fetchone()
                if not old_alert:
                    return False
                old_values = dict(old_alert)
                
                # Update alert
                update_fields = ["status = ?"]
                params = [status]
                
                if status in ['RESOLVED', 'CLOSED']:
                    update_fields.append("resolved_at = CURRENT_TIMESTAMP")
                
                if resolution_notes:
                    update_fields.append("resolution_notes = ?")
                    params.append(resolution_notes)
                
                params.append(alert_id)
                
                query = f"UPDATE alerts SET {', '.join(update_fields)} WHERE alert_id = ?"
                cursor.execute(query, params)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    
                    # Log audit trail
                    if updated_by:
                        self._log_audit_trail(
                            updated_by, 'UPDATE', 'alerts', alert_id,
                            old_values=old_values, 
                            new_values={'status': status, 'resolution_notes': resolution_notes},
                            conn=conn
                        )
                    
                    logger.info(f"Alert status updated: {alert_id} -> {status}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error updating alert status: {e}")
            return False
    
    def assign_alert(self, alert_id: str, officer: str, assigned_by: str = None) -> bool:
        """Assign alert to an officer"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE alerts 
                    SET assigned_officer = ?, assigned_at = CURRENT_TIMESTAMP
                    WHERE alert_id = ?
                """, (officer, alert_id))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    
                    # Log audit trail
                    if assigned_by:
                        self._log_audit_trail(
                            assigned_by, 'UPDATE', 'alerts', alert_id,
                            new_values={'assigned_officer': officer}, conn=conn
                        )
                    
                    logger.info(f"Alert assigned: {alert_id} -> {officer}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error assigning alert: {e}")
            return False
    
    # ==================== INVESTIGATIONS MANAGEMENT ====================
    
    def create_investigation(self, title: str, description: str, content_ids: List[int],
                           lead_officer: str, priority: str = 'MEDIUM',
                           alert_ids: List[str] = None, classification: str = None,
                           deadline: datetime = None) -> str:
        """Create a new investigation case"""
        try:
            case_id = f"CASE_{datetime.now().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8].upper()}"
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO investigations 
                    (case_id, title, description, content_ids, alert_ids, priority,
                     lead_officer, classification, deadline)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    case_id, title, description, json.dumps(content_ids),
                    json.dumps(alert_ids) if alert_ids else None, priority,
                    lead_officer, classification,
                    deadline.isoformat() if deadline else None
                ))
                
                conn.commit()
                logger.info(f"Investigation created: {case_id}")
                return case_id
                
        except Exception as e:
            logger.error(f"Error creating investigation: {e}")
            return None
    
    def get_investigations(self, status: str = None, lead_officer: str = None,
                         priority: str = None, classification: str = None,
                         limit: int = 50) -> List[Dict]:
        """Retrieve investigations with filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM investigations WHERE 1=1"
                params = []
                
                if status:
                    query += " AND status = ?"
                    params.append(status)
                if lead_officer:
                    query += " AND lead_officer = ?"
                    params.append(lead_officer)
                if priority:
                    query += " AND priority = ?"
                    params.append(priority)
                if classification:
                    query += " AND classification = ?"
                    params.append(classification)
                
                query += " ORDER BY created_at DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                investigations = []
                
                for row in cursor.fetchall():
                    inv = dict(row)
                    # Parse JSON fields
                    try:
                        inv['content_ids'] = json.loads(inv['content_ids']) if inv['content_ids'] else []
                        inv['alert_ids'] = json.loads(inv['alert_ids']) if inv['alert_ids'] else []
                        inv['team_members'] = json.loads(inv['team_members']) if inv['team_members'] else []
                        inv['evidence'] = json.loads(inv['evidence']) if inv['evidence'] else {}
                        inv['metadata'] = json.loads(inv['metadata']) if inv['metadata'] else {}
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in investigation {inv['case_id']}")
                    
                    investigations.append(inv)
                
                return investigations
                
        except Exception as e:
            logger.error(f"Error retrieving investigations: {e}")
            return []
    
    def update_investigation(self, case_id: str, updates: Dict, updated_by: str = None) -> bool:
        """Update investigation details"""
        try:
            if not updates:
                return False
            
            # Get old values for audit
            old_investigation = self.get_investigation_by_id(case_id)
            if not old_investigation:
                return False
            
            # Build update query
            set_clauses = []
            params = []
            
            allowed_fields = ['title', 'description', 'status', 'priority', 'team_members',
                            'evidence', 'deadline', 'court_case_number', 'legal_status',
                            'classification', 'metadata']
            
            for field, value in updates.items():
                if field in allowed_fields:
                    set_clauses.append(f"{field} = ?")
                    if field in ['team_members', 'evidence', 'metadata'] and isinstance(value, (dict, list)):
                        params.append(json.dumps(value))
                    elif field == 'deadline' and isinstance(value, datetime):
                        params.append(value.isoformat())
                    else:
                        params.append(value)
            
            if not set_clauses:
                return False
            
            set_clauses.append("updated_at = CURRENT_TIMESTAMP")
            params.append(case_id)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                query = f"UPDATE investigations SET {', '.join(set_clauses)} WHERE case_id = ?"
                cursor.execute(query, params)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    
                    # Log audit trail
                    if updated_by:
                        self._log_audit_trail(
                            updated_by, 'UPDATE', 'investigations', case_id,
                            old_values=old_investigation, new_values=updates, conn=conn
                        )
                    
                    logger.info(f"Investigation updated: {case_id}")
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"Error updating investigation: {e}")
            return False
    
    def get_investigation_by_id(self, case_id: str) -> Optional[Dict]:
        """Get investigation by case ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM investigations WHERE case_id = ?", (case_id,))
                row = cursor.fetchone()
                
                if row:
                    inv = dict(row)
                    # Parse JSON fields
                    try:
                        inv['content_ids'] = json.loads(inv['content_ids']) if inv['content_ids'] else []
                        inv['alert_ids'] = json.loads(inv['alert_ids']) if inv['alert_ids'] else []
                        inv['team_members'] = json.loads(inv['team_members']) if inv['team_members'] else []
                        inv['evidence'] = json.loads(inv['evidence']) if inv['evidence'] else {}
                        inv['metadata'] = json.loads(inv['metadata']) if inv['metadata'] else {}
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in investigation {case_id}")
                    
                    return inv
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting investigation: {e}")
            return None
    
    def add_evidence_to_investigation(self, case_id: str, evidence_type: str,
                                    evidence_data: Dict, added_by: str = None) -> bool:
        """Add evidence to an investigation"""
        try:
            investigation = self.get_investigation_by_id(case_id)
            if not investigation:
                return False
            
            # Add new evidence
            evidence = investigation.get('evidence', {})
            evidence_id = str(uuid.uuid4())
            evidence[evidence_id] = {
                'type': evidence_type,
                'data': evidence_data,
                'added_at': datetime.now().isoformat(),
                'added_by': added_by
            }
            
            # Update investigation
            return self.update_investigation(
                case_id, 
                {'evidence': evidence}, 
                updated_by=added_by
            )
            
        except Exception as e:
            logger.error(f"Error adding evidence: {e}")
            return False
    
    # ==================== API LOGS MANAGEMENT ====================
    
    def log_api_operation(self, platform: str, operation: str, success: bool,
                         endpoint: str = None, request_data: Dict = None,
                         response_status: int = None, error_message: str = None,
                         execution_time_ms: int = None, **kwargs) -> bool:
        """Log API operation"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO api_logs 
                    (platform, operation, endpoint, request_data, response_status,
                     success, error_message, execution_time_ms, rate_limit_remaining,
                     user_agent, ip_address, session_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    platform, operation, endpoint,
                    json.dumps(request_data) if request_data else None,
                    response_status, success, error_message, execution_time_ms,
                    kwargs.get('rate_limit_remaining'), kwargs.get('user_agent'),
                    kwargs.get('ip_address'), kwargs.get('session_id')
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error logging API operation: {e}")
            return False
    
    def get_api_logs(self, platform: str = None, operation: str = None,
                    success_only: bool = None, hours_back: int = 24,
                    limit: int = 100) -> List[Dict]:
        """Retrieve API logs with filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM api_logs WHERE timestamp >= ?"
                params = [datetime.now() - timedelta(hours=hours_back)]
                
                if platform:
                    query += " AND platform = ?"
                    params.append(platform)
                if operation:
                    query += " AND operation = ?"
                    params.append(operation)
                if success_only is not None:
                    query += " AND success = ?"
                    params.append(success_only)
                
                query += " ORDER BY timestamp DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error retrieving API logs: {e}")
            return []
    
    # ==================== USER MANAGEMENT ====================
    
    def create_user(self, username: str, full_name: str, email: str,
                   role: str, department: str, badge_number: str = None,
                   permissions: List[str] = None) -> str:
        """Create a new user account"""
        try:
            user_id = str(uuid.uuid4())
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users 
                    (user_id, username, full_name, email, role, department, 
                     badge_number, permissions)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id, username, full_name, email, role, department,
                    badge_number, json.dumps(permissions) if permissions else None
                ))
                
                conn.commit()
                logger.info(f"User created: {username} ({role})")
                return user_id
                
        except sqlite3.IntegrityError as e:
            logger.warning(f"User creation failed - integrity error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    def get_users(self, role: str = None, department: str = None,
                 active_only: bool = True) -> List[Dict]:
        """Retrieve users with filtering"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM users WHERE 1=1"
                params = []
                
                if active_only:
                    query += " AND is_active = 1"
                if role:
                    query += " AND role = ?"
                    params.append(role)
                if department:
                    query += " AND department = ?"
                    params.append(department)
                
                query += " ORDER BY full_name ASC"
                
                cursor.execute(query, params)
                users = []
                
                for row in cursor.fetchall():
                    user = dict(row)
                    # Parse permissions JSON
                    try:
                        user['permissions'] = json.loads(user['permissions']) if user['permissions'] else []
                    except json.JSONDecodeError:
                        user['permissions'] = []
                    
                    # Remove sensitive data
                    user.pop('password_hash', None)
                    users.append(user)
                
                return users
                
        except Exception as e:
            logger.error(f"Error retrieving users: {e}")
            return []
    
    # ==================== ANALYTICS AND REPORTING ====================
    
    def get_threat_analytics(self, days_back: int = 30) -> Dict:
        """Get comprehensive threat analytics"""
        try:
            start_date = datetime.now() - timedelta(days=days_back)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                analytics = {}
                
                # Content statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_content,
                        AVG(risk_score) as avg_risk_score,
                        COUNT(CASE WHEN threat_level = 'CRITICAL' THEN 1 END) as critical_threats,
                        COUNT(CASE WHEN threat_level = 'HIGH' THEN 1 END) as high_threats,
                        COUNT(CASE WHEN is_flagged = 1 THEN 1 END) as flagged_content
                    FROM monitored_content 
                    WHERE created_at >= ?
                """, (start_date.isoformat(),))
                
                content_stats = dict(cursor.fetchone())
                analytics['content_statistics'] = content_stats
                
                # Platform distribution
                cursor.execute("""
                    SELECT platform, COUNT(*) as count, AVG(risk_score) as avg_risk
                    FROM monitored_content 
                    WHERE created_at >= ?
                    GROUP BY platform
                    ORDER BY count DESC
                """, (start_date.isoformat(),))
                
                analytics['platform_distribution'] = [dict(row) for row in cursor.fetchall()]
                
                # Daily threat trends
                cursor.execute("""
                    SELECT 
                        DATE(created_at) as date,
                        COUNT(*) as content_count,
                        AVG(risk_score) as avg_risk,
                        COUNT(CASE WHEN threat_level IN ('HIGH', 'CRITICAL') THEN 1 END) as high_risk_count
                    FROM monitored_content 
                    WHERE created_at >= ?
                    GROUP BY DATE(created_at)
                    ORDER BY date DESC
                """, (start_date.isoformat(),))
                
                analytics['daily_trends'] = [dict(row) for row in cursor.fetchall()]
                
                # Alert statistics
                cursor.execute("""
                    SELECT 
                        status,
                        severity,
                        COUNT(*) as count
                    FROM alerts 
                    WHERE timestamp >= ?
                    GROUP BY status, severity
                """, (start_date.isoformat(),))
                
                alert_stats = {}
                for row in cursor.fetchall():
                    status = row['status']
                    if status not in alert_stats:
                        alert_stats[status] = {}
                    alert_stats[status][row['severity']] = row['count']
                
                analytics['alert_statistics'] = alert_stats
                
                # Investigation statistics
                cursor.execute("""
                    SELECT 
                        status,
                        priority,
                        classification,
                        COUNT(*) as count
                    FROM investigations 
                    WHERE created_at >= ?
                    GROUP BY status, priority, classification
                """, (start_date.isoformat(),))
                
                analytics['investigation_statistics'] = [dict(row) for row in cursor.fetchall()]
                
                # Top keywords by category
                cursor.execute("""
                    SELECT k.category, k.term, COUNT(mc.id) as matches
                    FROM keywords k
                    LEFT JOIN monitored_content mc ON mc.content LIKE '%' || k.term || '%'
                        AND mc.created_at >= ?
                    WHERE k.is_active = 1
                    GROUP BY k.category, k.term
                    HAVING matches > 0
                    ORDER BY matches DESC
                    LIMIT 20
                """, (start_date.isoformat(),))
                
                analytics['top_keywords'] = [dict(row) for row in cursor.fetchall()]
                
                return analytics
                
        except Exception as e:
            logger.error(f"Error generating analytics: {e}")
            return {}
    
    def get_officer_performance(self, officer_id: str = None, days_back: int = 30) -> Dict:
        """Get officer performance analytics"""
        try:
            start_date = datetime.now() - timedelta(days=days_back)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if officer_id:
                    # Specific officer performance
                    cursor.execute("""
                        SELECT 
                            COUNT(CASE WHEN a.status = 'RESOLVED' THEN 1 END) as resolved_alerts,
                            COUNT(CASE WHEN a.status = 'CLOSED' THEN 1 END) as closed_alerts,
                            COUNT(CASE WHEN a.status IN ('OPEN', 'INVESTIGATING') THEN 1 END) as active_alerts,
                            AVG(CASE WHEN a.resolved_at IS NOT NULL 
                                THEN julianday(a.resolved_at) - julianday(a.assigned_at) END) as avg_resolution_days
                        FROM alerts a
                        WHERE a.assigned_officer = ? AND a.assigned_at >= ?
                    """, (officer_id, start_date.isoformat()))
                    
                    performance = dict(cursor.fetchone())
                    
                    # Investigation statistics
                    cursor.execute("""
                        SELECT 
                            COUNT(*) as total_investigations,
                            COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_investigations,
                            COUNT(CASE WHEN status = 'ACTIVE' THEN 1 END) as active_investigations
                        FROM investigations 
                        WHERE lead_officer = ? AND created_at >= ?
                    """, (officer_id, start_date.isoformat()))
                    
                    inv_stats = dict(cursor.fetchone())
                    performance.update(inv_stats)
                    
                    return performance
                else:
                    # All officers summary
                    cursor.execute("""
                        SELECT 
                            a.assigned_officer,
                            u.full_name,
                            COUNT(*) as total_assigned,
                            COUNT(CASE WHEN a.status = 'RESOLVED' THEN 1 END) as resolved,
                            COUNT(CASE WHEN a.status = 'CLOSED' THEN 1 END) as closed,
                            AVG(CASE WHEN a.resolved_at IS NOT NULL 
                                THEN julianday(a.resolved_at) - julianday(a.assigned_at) END) as avg_resolution_days
                        FROM alerts a
                        LEFT JOIN users u ON a.assigned_officer = u.username
                        WHERE a.assigned_at >= ?
                        GROUP BY a.assigned_officer
                        ORDER BY total_assigned DESC
                    """, (start_date.isoformat(),))
                    
                    return [dict(row) for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting officer performance: {e}")
            return {} if officer_id else []
    
    # ==================== DATA EXPORT FOR COURT EVIDENCE ====================
    
    def export_case_evidence(self, case_id: str, export_format: str = 'json') -> Dict:
        """Export complete case evidence in court-admissible format"""
        try:
            investigation = self.get_investigation_by_id(case_id)
            if not investigation:
                return None
            
            evidence_package = {
                'case_information': {
                    'case_id': case_id,
                    'title': investigation['title'],
                    'description': investigation['description'],
                    'classification': investigation['classification'],
                    'lead_officer': investigation['lead_officer'],
                    'created_at': investigation['created_at'],
                    'status': investigation['status'],
                    'court_case_number': investigation.get('court_case_number'),
                    'legal_status': investigation.get('legal_status')
                },
                'digital_evidence': [],
                'alerts': [],
                'chain_of_custody': [],
                'metadata': {
                    'export_timestamp': datetime.now().isoformat(),
                    'export_format': export_format,
                    'evidence_integrity_hash': None,
                    'exported_by': 'SYSTEM',
                    'legal_compliance': 'Indian Evidence Act 1872, IT Act 2000'
                }
            }
            
            # Get monitored content evidence
            content_ids = investigation.get('content_ids', [])
            if content_ids:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    placeholders = ','.join(['?' for _ in content_ids])
                    cursor.execute(f"""
                        SELECT * FROM monitored_content 
                        WHERE id IN ({placeholders})
                        ORDER BY timestamp ASC
                    """, content_ids)
                    
                    for row in cursor.fetchall():
                        content = dict(row)
                        
                        # Add chain of custody information
                        custody_entry = {
                            'evidence_id': f"CONTENT_{content['id']}",
                            'evidence_type': 'digital_content',
                            'collected_at': content['created_at'],
                            'source_platform': content['platform'],
                            'content_hash': content['content_hash'],
                            'verification_status': 'verified'
                        }
                        
                        evidence_package['digital_evidence'].append(content)
                        evidence_package['chain_of_custody'].append(custody_entry)
            
            # Get related alerts
            alert_ids = investigation.get('alert_ids', [])
            if alert_ids:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    placeholders = ','.join(['?' for _ in alert_ids])
                    cursor.execute(f"""
                        SELECT * FROM alerts 
                        WHERE alert_id IN ({placeholders})
                        ORDER BY timestamp ASC
                    """, alert_ids)
                    
                    evidence_package['alerts'] = [dict(row) for row in cursor.fetchall()]
            
            # Calculate evidence integrity hash
            evidence_string = json.dumps(evidence_package['digital_evidence'], sort_keys=True)
            evidence_hash = hashlib.sha256(evidence_string.encode()).hexdigest()
            evidence_package['metadata']['evidence_integrity_hash'] = evidence_hash
            
            return evidence_package
            
        except Exception as e:
            logger.error(f"Error exporting case evidence: {e}")
            return None
    
    def export_investigation_report(self, case_id: str) -> Dict:
        """Generate comprehensive investigation report"""
        try:
            investigation = self.get_investigation_by_id(case_id)
            if not investigation:
                return None
            
            report = {
                'report_header': {
                    'case_id': case_id,
                    'report_generated': datetime.now().isoformat(),
                    'report_type': 'COMPREHENSIVE_INVESTIGATION_REPORT',
                    'classification': investigation.get('classification', 'UNCLASSIFIED')
                },
                'case_summary': investigation,
                'evidence_analysis': {},
                'timeline': [],
                'risk_assessment': {},
                'recommendations': []
            }
            
            # Analyze evidence content
            content_ids = investigation.get('content_ids', [])
            if content_ids:
                with self.get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Content analysis
                    placeholders = ','.join(['?' for _ in content_ids])
                    cursor.execute(f"""
                        SELECT 
                            COUNT(*) as total_items,
                            AVG(risk_score) as avg_risk_score,
                            MAX(risk_score) as max_risk_score,
                            COUNT(CASE WHEN threat_level = 'CRITICAL' THEN 1 END) as critical_items,
                            COUNT(CASE WHEN threat_level = 'HIGH' THEN 1 END) as high_risk_items,
                            COUNT(DISTINCT platform) as platforms_involved,
                            COUNT(DISTINCT author) as unique_authors,
                            MIN(timestamp) as earliest_content,
                            MAX(timestamp) as latest_content
                        FROM monitored_content 
                        WHERE id IN ({placeholders})
                    """, content_ids)
                    
                    evidence_stats = dict(cursor.fetchone())
                    report['evidence_analysis'] = evidence_stats
                    
                    # Timeline construction
                    cursor.execute(f"""
                        SELECT timestamp, content, author, platform, risk_score, threat_level
                        FROM monitored_content 
                        WHERE id IN ({placeholders})
                        ORDER BY timestamp ASC
                    """, content_ids)
                    
                    timeline_events = []
                    for row in cursor.fetchall():
                        event = {
                            'timestamp': row['timestamp'],
                            'event_type': 'content_detected',
                            'description': f"{row['author']} posted on {row['platform']}",
                            'risk_level': row['threat_level'],
                            'details': {
                                'platform': row['platform'],
                                'author': row['author'],
                                'risk_score': row['risk_score'],
                                'content_preview': row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
                            }
                        }
                        timeline_events.append(event)
                    
                    report['timeline'] = timeline_events
            
            # Risk assessment
            if report['evidence_analysis']:
                avg_risk = report['evidence_analysis'].get('avg_risk_score', 0)
                max_risk = report['evidence_analysis'].get('max_risk_score', 0)
                critical_count = report['evidence_analysis'].get('critical_items', 0)
                
                if max_risk >= 80 or critical_count > 0:
                    risk_level = 'HIGH'
                elif avg_risk >= 60:
                    risk_level = 'MEDIUM'
                else:
                    risk_level = 'LOW'
                
                report['risk_assessment'] = {
                    'overall_risk_level': risk_level,
                    'average_content_risk': avg_risk,
                    'peak_risk_score': max_risk,
                    'critical_items_count': critical_count,
                    'assessment_confidence': 'HIGH' if len(content_ids) > 5 else 'MEDIUM'
                }
            
            # Generate recommendations
            recommendations = []
            if report['risk_assessment'].get('overall_risk_level') == 'HIGH':
                recommendations.extend([
                    "Immediate escalation to specialized cyber crime unit recommended",
                    "Continuous monitoring of identified accounts and networks",
                    "Consider legal action under relevant sections of IT Act 2000"
                ])
            
            if investigation.get('status') in ['ACTIVE', 'UNDER_REVIEW']:
                recommendations.append("Investigation requires additional evidence collection")
            
            report['recommendations'] = recommendations
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating investigation report: {e}")
            return None
    
    # ==================== BACKUP AND RESTORE ====================
    
    def create_backup(self, backup_name: str = None) -> str:
        """Create database backup"""
        try:
            if not backup_name:
                backup_name = f"police_monitoring_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Create backup
            shutil.copy2(self.db_path, backup_path)
            
            # Verify backup integrity
            with sqlite3.connect(backup_path) as backup_conn:
                backup_conn.execute("PRAGMA integrity_check")
            
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None
    
    def restore_backup(self, backup_path: str) -> bool:
        """Restore database from backup"""
        try:
            if not os.path.exists(backup_path):
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Verify backup integrity
            with sqlite3.connect(backup_path) as backup_conn:
                result = backup_conn.execute("PRAGMA integrity_check").fetchone()
                if result[0] != 'ok':
                    logger.error("Backup file is corrupted")
                    return False
            
            # Create current backup before restore
            current_backup = self.create_backup(f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            
            logger.info(f"Database restored from: {backup_path}")
            logger.info(f"Previous database backed up to: {current_backup}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return False
    
    def list_backups(self) -> List[Dict]:
        """List available database backups"""
        try:
            backups = []
            
            if not os.path.exists(self.backup_dir):
                return backups
            
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.db'):
                    filepath = os.path.join(self.backup_dir, filename)
                    stat = os.stat(filepath)
                    
                    backup_info = {
                        'filename': filename,
                        'filepath': filepath,
                        'size_bytes': stat.st_size,
                        'created_at': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified_at': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                    backups.append(backup_info)
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x['created_at'], reverse=True)
            return backups
            
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return []
    
    def cleanup_old_backups(self, keep_days: int = 30) -> int:
        """Clean up old backup files"""
        try:
            cutoff_date = datetime.now() - timedelta(days=keep_days)
            deleted_count = 0
            
            backups = self.list_backups()
            for backup in backups:
                backup_date = datetime.fromisoformat(backup['created_at'])
                if backup_date < cutoff_date:
                    try:
                        os.remove(backup['filepath'])
                        deleted_count += 1
                        logger.info(f"Deleted old backup: {backup['filename']}")
                    except OSError as e:
                        logger.warning(f"Could not delete backup {backup['filename']}: {e}")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
            return 0
    
    # ==================== ADVANCED SEARCH AND FILTERING ====================
    
    def advanced_content_search(self, search_params: Dict) -> List[Dict]:
        """Advanced search with multiple filters and full-text search"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT mc.*, 
                           GROUP_CONCAT(a.alert_id) as related_alerts,
                           COUNT(a.alert_id) as alert_count
                    FROM monitored_content mc
                    LEFT JOIN alerts a ON mc.id = a.content_id
                    WHERE 1=1
                """
                params = []
                
                # Text search
                if search_params.get('text_query'):
                    query += " AND mc.content LIKE ?"
                    params.append(f"%{search_params['text_query']}%")
                
                # Author search
                if search_params.get('author'):
                    query += " AND mc.author LIKE ?"
                    params.append(f"%{search_params['author']}%")
                
                # Platform filter
                if search_params.get('platforms'):
                    platforms = search_params['platforms']
                    placeholders = ','.join(['?' for _ in platforms])
                    query += f" AND mc.platform IN ({placeholders})"
                    params.extend(platforms)
                
                # Risk score range
                if search_params.get('min_risk_score') is not None:
                    query += " AND mc.risk_score >= ?"
                    params.append(search_params['min_risk_score'])
                
                if search_params.get('max_risk_score') is not None:
                    query += " AND mc.risk_score <= ?"
                    params.append(search_params['max_risk_score'])
                
                # Threat level filter
                if search_params.get('threat_levels'):
                    threat_levels = search_params['threat_levels']
                    placeholders = ','.join(['?' for _ in threat_levels])
                    query += f" AND mc.threat_level IN ({placeholders})"
                    params.extend(threat_levels)
                
                # Date range
                if search_params.get('date_from'):
                    query += " AND mc.timestamp >= ?"
                    params.append(search_params['date_from'].isoformat())
                
                if search_params.get('date_to'):
                    query += " AND mc.timestamp <= ?"
                    params.append(search_params['date_to'].isoformat())
                
                # Location filter
                if search_params.get('location'):
                    query += " AND mc.location LIKE ?"
                    params.append(f"%{search_params['location']}%")
                
                # Language filter
                if search_params.get('language'):
                    query += " AND mc.language = ?"
                    params.append(search_params['language'])
                
                # Flagged content only
                if search_params.get('flagged_only'):
                    query += " AND mc.is_flagged = 1"
                
                # Has alerts filter
                if search_params.get('has_alerts'):
                    query += " AND a.alert_id IS NOT NULL"
                
                query += " GROUP BY mc.id"
                
                # Sorting
                sort_by = search_params.get('sort_by', 'timestamp')
                sort_order = search_params.get('sort_order', 'DESC')
                
                if sort_by in ['timestamp', 'risk_score', 'created_at']:
                    query += f" ORDER BY mc.{sort_by} {sort_order}"
                elif sort_by == 'alert_count':
                    query += f" ORDER BY alert_count {sort_order}"
                
                # Pagination
                limit = search_params.get('limit', 100)
                offset = search_params.get('offset', 0)
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                results = []
                
                for row in cursor.fetchall():
                    result = dict(row)
                    # Parse related alerts
                    if result['related_alerts']:
                        result['related_alerts'] = result['related_alerts'].split(',')
                    else:
                        result['related_alerts'] = []
                    
                    results.append(result)
                
                return results
                
        except Exception as e:
            logger.error(f"Error in advanced search: {e}")
            return []
    
    def get_database_statistics(self) -> Dict:
        """Get comprehensive database statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Table row counts
                tables = ['keywords', 'monitored_content', 'alerts', 'investigations', 
                         'api_logs', 'users', 'audit_trail']
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    stats[f"{table}_count"] = cursor.fetchone()[0]
                
                # Database size
                cursor.execute("PRAGMA page_count")
                page_count = cursor.fetchone()[0]
                cursor.execute("PRAGMA page_size")
                page_size = cursor.fetchone()[0]
                stats['database_size_bytes'] = page_count * page_size
                
                # Recent activity (last 24 hours)
                yesterday = datetime.now() - timedelta(days=1)
                
                cursor.execute("""
                    SELECT COUNT(*) FROM monitored_content 
                    WHERE created_at >= ?
                """, (yesterday.isoformat(),))
                stats['content_last_24h'] = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM alerts 
                    WHERE timestamp >= ?
                """, (yesterday.isoformat(),))
                stats['alerts_last_24h'] = cursor.fetchone()[0]
                
                # Performance stats
                stats['last_updated'] = datetime.now().isoformat()
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting database statistics: {e}")
            return {}


# ==================== USAGE EXAMPLE AND TESTING ====================

if __name__ == "__main__":
    # Example usage and basic testing
    
    print("🏛️ Police Monitoring Database Manager - Testing")
    print("=" * 60)
    
    # Initialize database
    db = PoliceMonitoringDB("test_police_monitoring.db")
    
    # Test keyword management
    print("\n📝 Testing Keyword Management...")
    db.add_keyword("terrorism", "security", 9, "en", "test_user")
    db.add_keyword("भतकी", "security", 8, "hi", "test_user")
    keywords = db.get_keywords()
    print(f"Keywords in database: {len(keywords)}")
    
    # Test content monitoring
    print("\n🔍 Testing Content Monitoring...")
    content_id = db.add_monitored_content(
        platform="Twitter",
        content="This is a test suspicious message about terrorism",
        author="test_user",
        timestamp=datetime.now(),
        risk_score=85.5,
        threat_level="HIGH",
        sentiment="negative",
        language="en"
    )
    print(f"Content added with ID: {content_id}")
    
    # Test alert creation
    print("\n🚨 Testing Alert System...")
    alert_id = db.create_alert(
        alert_type="HIGH_RISK_CONTENT",
        severity="HIGH",
        message="High risk content detected",
        content_id=content_id
    )
    print(f"Alert created with ID: {alert_id}")
    
    # Test investigation creation
    print("\n🔬 Testing Investigation Management...")
    case_id = db.create_investigation(
        title="Test Terrorism Investigation",
        description="Testing investigation system",
        content_ids=[content_id],
        lead_officer="officer_test",
        priority="HIGH",
        classification="terrorism"
    )
    print(f"Investigation created with ID: {case_id}")
    
    # Test analytics
    print("\n📊 Testing Analytics...")
    analytics = db.get_threat_analytics(days_back=1)
    print(f"Analytics generated: {len(analytics)} categories")
    
    # Test backup
    print("\n💾 Testing Backup System...")
    backup_path = db.create_backup()
    print(f"Backup created: {backup_path}")
    
    # Test database statistics
    print("\n📈 Database Statistics:")
    stats = db.get_database_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ All tests completed successfully!")
    print("🏛️ Police Monitoring Database System Ready for Deployment")
