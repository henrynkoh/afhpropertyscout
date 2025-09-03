"""
Database Manager - Handles data storage and retrieval for AFH properties
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from loguru import logger
import pandas as pd
from pathlib import Path

class DatabaseManager:
    """Manages database operations for AFH property data"""
    
    def __init__(self, db_config: Dict[str, Any]):
        """Initialize database manager with configuration"""
        self.db_config = db_config
        self.db_path = db_config.get('path', 'data/afh_properties.db')
        
        # Create database directory if it doesn't exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Properties table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS properties (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source TEXT NOT NULL,
                        listing_id TEXT,
                        address TEXT NOT NULL,
                        city TEXT,
                        state TEXT DEFAULT 'WA',
                        zip_code TEXT,
                        county TEXT,
                        price REAL,
                        bedrooms INTEGER,
                        bathrooms INTEGER,
                        sqft INTEGER,
                        property_type TEXT,
                        description TEXT,
                        wabo_status TEXT,
                        url TEXT,
                        images TEXT,  -- JSON array
                        date_listed TEXT,
                        contact_info TEXT,  -- JSON object
                        raw_data TEXT,  -- JSON object
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(source, listing_id, address)
                    )
                ''')
                
                # Property analysis table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS property_analysis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        property_id INTEGER,
                        viable BOOLEAN,
                        viability_score REAL,
                        basic_analysis TEXT,  -- JSON object
                        financial_analysis TEXT,  -- JSON object
                        market_analysis TEXT,  -- JSON object
                        wabo_analysis TEXT,  -- JSON object
                        risk_analysis TEXT,  -- JSON object
                        pricing_analysis TEXT,  -- JSON object
                        recommendations TEXT,  -- JSON array
                        analysis_date TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (property_id) REFERENCES properties (id)
                    )
                ''')
                
                # Notifications table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        property_id INTEGER,
                        notification_type TEXT,  -- 'email', 'sms', 'both'
                        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status TEXT DEFAULT 'sent',  -- 'sent', 'failed', 'pending'
                        error_message TEXT,
                        FOREIGN KEY (property_id) REFERENCES properties (id)
                    )
                ''')
                
                # Search history table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS search_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        total_properties_found INTEGER,
                        viable_properties_found INTEGER,
                        new_properties_found INTEGER,
                        sources_searched TEXT,  -- JSON array
                        search_duration_seconds REAL,
                        status TEXT DEFAULT 'completed'  -- 'completed', 'failed', 'partial'
                    )
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_properties_address ON properties(address)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_properties_county ON properties(county)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_properties_price ON properties(price)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_properties_created_at ON properties(created_at)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_viable ON property_analysis(viable)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_score ON property_analysis(viability_score)')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def store_properties(self, analyzed_properties: List[Dict[str, Any]]) -> int:
        """Store analyzed properties in database"""
        try:
            stored_count = 0
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for property_data in analyzed_properties:
                    try:
                        prop = property_data['property']
                        analysis = property_data['analysis']
                        
                        # Insert or update property
                        property_id = self._upsert_property(cursor, prop)
                        
                        # Insert analysis
                        self._insert_analysis(cursor, property_id, analysis)
                        
                        stored_count += 1
                        
                    except Exception as e:
                        logger.warning(f"Error storing property: {e}")
                        continue
                
                conn.commit()
                logger.info(f"Stored {stored_count} properties with analysis")
                
        except Exception as e:
            logger.error(f"Error storing properties: {e}")
            raise
        
        return stored_count
    
    def _upsert_property(self, cursor, property_data: Dict[str, Any]) -> int:
        """Insert or update property and return property ID"""
        # Check if property already exists
        cursor.execute('''
            SELECT id FROM properties 
            WHERE source = ? AND listing_id = ? AND address = ?
        ''', (
            property_data.get('source', ''),
            property_data.get('listing_id', ''),
            property_data.get('address', '')
        ))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing property
            property_id = existing[0]
            cursor.execute('''
                UPDATE properties SET
                    price = ?, bedrooms = ?, bathrooms = ?, sqft = ?,
                    property_type = ?, description = ?, wabo_status = ?,
                    url = ?, images = ?, date_listed = ?, contact_info = ?,
                    raw_data = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                property_data.get('price', 0),
                property_data.get('bedrooms', 0),
                property_data.get('bathrooms', 0),
                property_data.get('sqft', 0),
                property_data.get('property_type', ''),
                property_data.get('description', ''),
                property_data.get('wabo_status', ''),
                property_data.get('url', ''),
                json.dumps(property_data.get('images', [])),
                property_data.get('date_listed', ''),
                json.dumps(property_data.get('contact_info', {})),
                json.dumps(property_data.get('raw_data', {})),
                property_id
            ))
        else:
            # Insert new property
            cursor.execute('''
                INSERT INTO properties (
                    source, listing_id, address, city, state, zip_code, county,
                    price, bedrooms, bathrooms, sqft, property_type, description,
                    wabo_status, url, images, date_listed, contact_info, raw_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                property_data.get('source', ''),
                property_data.get('listing_id', ''),
                property_data.get('address', ''),
                property_data.get('city', ''),
                property_data.get('state', 'WA'),
                property_data.get('zip_code', ''),
                property_data.get('county', ''),
                property_data.get('price', 0),
                property_data.get('bedrooms', 0),
                property_data.get('bathrooms', 0),
                property_data.get('sqft', 0),
                property_data.get('property_type', ''),
                property_data.get('description', ''),
                property_data.get('wabo_status', ''),
                property_data.get('url', ''),
                json.dumps(property_data.get('images', [])),
                property_data.get('date_listed', ''),
                json.dumps(property_data.get('contact_info', {})),
                json.dumps(property_data.get('raw_data', {}))
            ))
            property_id = cursor.lastrowid
        
        return property_id
    
    def _insert_analysis(self, cursor, property_id: int, analysis: Dict[str, Any]):
        """Insert property analysis"""
        cursor.execute('''
            INSERT INTO property_analysis (
                property_id, viable, viability_score, basic_analysis,
                financial_analysis, market_analysis, wabo_analysis,
                risk_analysis, pricing_analysis, recommendations, analysis_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            property_id,
            analysis.get('viable', False),
            analysis.get('viability_score', 0),
            json.dumps(analysis.get('basic_analysis', {})),
            json.dumps(analysis.get('financial_analysis', {})),
            json.dumps(analysis.get('market_analysis', {})),
            json.dumps(analysis.get('wabo_analysis', {})),
            json.dumps(analysis.get('risk_analysis', {})),
            json.dumps(analysis.get('pricing_analysis', {})),
            json.dumps(analysis.get('recommendations', [])),
            analysis.get('analysis_date', datetime.now().isoformat())
        ))
    
    def get_new_properties(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get properties that are new within the specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT p.*, pa.viable, pa.viability_score, pa.basic_analysis,
                           pa.financial_analysis, pa.market_analysis, pa.wabo_analysis,
                           pa.risk_analysis, pa.pricing_analysis, pa.recommendations
                    FROM properties p
                    JOIN property_analysis pa ON p.id = pa.property_id
                    WHERE p.created_at > ? AND pa.viable = 1
                    ORDER BY pa.viability_score DESC
                ''', (cutoff_time.isoformat(),))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                properties = []
                for row in rows:
                    property_dict = dict(zip(columns, row))
                    
                    # Parse JSON fields
                    property_dict['images'] = json.loads(property_dict.get('images', '[]'))
                    property_dict['contact_info'] = json.loads(property_dict.get('contact_info', '{}'))
                    property_dict['raw_data'] = json.loads(property_dict.get('raw_data', '{}'))
                    property_dict['basic_analysis'] = json.loads(property_dict.get('basic_analysis', '{}'))
                    property_dict['financial_analysis'] = json.loads(property_dict.get('financial_analysis', '{}'))
                    property_dict['market_analysis'] = json.loads(property_dict.get('market_analysis', '{}'))
                    property_dict['wabo_analysis'] = json.loads(property_dict.get('wabo_analysis', '{}'))
                    property_dict['risk_analysis'] = json.loads(property_dict.get('risk_analysis', '{}'))
                    property_dict['pricing_analysis'] = json.loads(property_dict.get('pricing_analysis', '{}'))
                    property_dict['recommendations'] = json.loads(property_dict.get('recommendations', '[]'))
                    
                    properties.append(property_dict)
                
                logger.info(f"Found {len(properties)} new viable properties")
                return properties
                
        except Exception as e:
            logger.error(f"Error getting new properties: {e}")
            return []
    
    def get_property_summary(self) -> Dict[str, Any]:
        """Get summary of all properties in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total properties
                cursor.execute('SELECT COUNT(*) FROM properties')
                total = cursor.fetchone()[0]
                
                # Viable properties
                cursor.execute('SELECT COUNT(*) FROM property_analysis WHERE viable = 1')
                viable = cursor.fetchone()[0]
                
                # New properties (last 24 hours)
                cutoff_time = datetime.now() - timedelta(hours=24)
                cursor.execute('''
                    SELECT COUNT(*) FROM properties 
                    WHERE created_at > ?
                ''', (cutoff_time.isoformat(),))
                new = cursor.fetchone()[0]
                
                # Properties by county
                cursor.execute('''
                    SELECT county, COUNT(*) 
                    FROM properties 
                    GROUP BY county 
                    ORDER BY COUNT(*) DESC
                ''')
                county_distribution = dict(cursor.fetchall())
                
                # Properties by WABO status
                cursor.execute('''
                    SELECT wabo_status, COUNT(*) 
                    FROM properties 
                    GROUP BY wabo_status 
                    ORDER BY COUNT(*) DESC
                ''')
                wabo_distribution = dict(cursor.fetchall())
                
                # Average viability score
                cursor.execute('SELECT AVG(viability_score) FROM property_analysis')
                avg_score = cursor.fetchone()[0] or 0
                
                return {
                    'total': total,
                    'viable': viable,
                    'new': new,
                    'county_distribution': county_distribution,
                    'wabo_distribution': wabo_distribution,
                    'average_viability_score': round(avg_score, 1),
                    'last_updated': datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error getting property summary: {e}")
            return {
                'total': 0,
                'viable': 0,
                'new': 0,
                'error': str(e)
            }
    
    def get_top_properties(self, limit: int = 10, min_score: float = 70.0) -> List[Dict[str, Any]]:
        """Get top properties by viability score"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT p.*, pa.viable, pa.viability_score, pa.basic_analysis,
                           pa.financial_analysis, pa.market_analysis, pa.wabo_analysis,
                           pa.risk_analysis, pa.pricing_analysis, pa.recommendations
                    FROM properties p
                    JOIN property_analysis pa ON p.id = pa.property_id
                    WHERE pa.viability_score >= ?
                    ORDER BY pa.viability_score DESC
                    LIMIT ?
                ''', (min_score, limit))
                
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                properties = []
                for row in rows:
                    property_dict = dict(zip(columns, row))
                    
                    # Parse JSON fields
                    for json_field in ['images', 'contact_info', 'raw_data', 'basic_analysis',
                                     'financial_analysis', 'market_analysis', 'wabo_analysis',
                                     'risk_analysis', 'pricing_analysis', 'recommendations']:
                        if property_dict.get(json_field):
                            property_dict[json_field] = json.loads(property_dict[json_field])
                    
                    properties.append(property_dict)
                
                return properties
                
        except Exception as e:
            logger.error(f"Error getting top properties: {e}")
            return []
    
    def record_search_history(self, search_data: Dict[str, Any]):
        """Record search history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO search_history (
                        total_properties_found, viable_properties_found,
                        new_properties_found, sources_searched,
                        search_duration_seconds, status
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    search_data.get('total_properties', 0),
                    search_data.get('viable_properties', 0),
                    search_data.get('new_properties', 0),
                    json.dumps(search_data.get('sources_searched', [])),
                    search_data.get('duration_seconds', 0),
                    search_data.get('status', 'completed')
                ))
                
                conn.commit()
                logger.info("Search history recorded")
                
        except Exception as e:
            logger.error(f"Error recording search history: {e}")
    
    def record_notification(self, property_id: int, notification_type: str, 
                          status: str = 'sent', error_message: str = None):
        """Record notification sent"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO notifications (
                        property_id, notification_type, status, error_message
                    ) VALUES (?, ?, ?, ?)
                ''', (property_id, notification_type, status, error_message))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error recording notification: {e}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Table counts
                tables = ['properties', 'property_analysis', 'notifications', 'search_history']
                for table in tables:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    stats[f'{table}_count'] = cursor.fetchone()[0]
                
                # Recent activity
                cursor.execute('''
                    SELECT COUNT(*) FROM properties 
                    WHERE created_at > datetime('now', '-7 days')
                ''')
                stats['properties_last_7_days'] = cursor.fetchone()[0]
                
                # Viability distribution
                cursor.execute('''
                    SELECT 
                        CASE 
                            WHEN viability_score >= 90 THEN 'Excellent (90-100)'
                            WHEN viability_score >= 80 THEN 'Good (80-89)'
                            WHEN viability_score >= 70 THEN 'Fair (70-79)'
                            WHEN viability_score >= 60 THEN 'Poor (60-69)'
                            ELSE 'Very Poor (<60)'
                        END as score_range,
                        COUNT(*) as count
                    FROM property_analysis
                    GROUP BY score_range
                    ORDER BY MIN(viability_score) DESC
                ''')
                stats['viability_distribution'] = dict(cursor.fetchall())
                
                # Database size
                cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
                db_size = cursor.fetchone()[0]
                stats['database_size_bytes'] = db_size
                stats['database_size_mb'] = round(db_size / (1024 * 1024), 2)
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {'error': str(e)}
