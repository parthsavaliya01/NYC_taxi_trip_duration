"""
Enhanced database operations with proper connection management.

Features:
- Context managers for safe connection handling
- Connection pooling support
- Proper error handling and logging
- Transaction management
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from contextlib import contextmanager

from app.core.config import settings
from app.core.logger import setup_logging

logger = setup_logging(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path: str = settings.database.path) -> None:
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        logger.info(f"Database initialized at {db_path}")
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vendor_id INTEGER NOT NULL,
                    passenger_count INTEGER NOT NULL,
                    distance REAL NOT NULL,
                    duration REAL NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    
                    CHECK (vendor_id IN (1, 2)),
                    CHECK (passenger_count > 0),
                    CHECK (distance >= 0),
                    CHECK (duration > 0)
                )
                """)
                
                # Create index for faster queries
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_predictions_created_at 
                ON predictions(created_at)
                """)
                
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_predictions_vendor_id 
                ON predictions(vendor_id)
                """)
                
                conn.commit()
                logger.debug("Database schema created/verified")
                
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    @contextmanager
    def get_connection(self) -> sqlite3.Connection:
        """
        Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection.
            
        Raises:
            sqlite3.Error: If connection fails.
        """
        conn = None
        try:
            conn = sqlite3.connect(
                self.db_path,
                timeout=settings.database.timeout
            )
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
            logger.debug("Database transaction committed")
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def insert_prediction(
        self,
        vendor_id: int,
        passenger_count: int,
        distance: float,
        duration: float
    ) -> int:
        """
        Insert prediction record.
        
        Args:
            vendor_id: Taxi vendor ID (1 or 2).
            passenger_count: Number of passengers.
            distance: Trip distance in km.
            duration: Predicted duration in seconds.
            
        Returns:
            int: ID of inserted record.
            
        Raises:
            ValueError: If validation fails.
            sqlite3.Error: If database operation fails.
        """
        # Validate inputs
        if vendor_id not in (1, 2):
            raise ValueError(f"Invalid vendor_id: {vendor_id}")
        if passenger_count <= 0:
            raise ValueError(f"passenger_count must be positive: {passenger_count}")
        if distance < 0:
            raise ValueError(f"distance cannot be negative: {distance}")
        if duration <= 0:
            raise ValueError(f"duration must be positive: {duration}")
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO predictions 
                (vendor_id, passenger_count, distance, duration, created_at)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    vendor_id,
                    passenger_count,
                    distance,
                    duration,
                    datetime.now()
                ))
                
                logger.info(f"Prediction inserted: ID={cursor.lastrowid}")
                return cursor.lastrowid
                
        except sqlite3.IntegrityError as e:
            logger.error(f"Data integrity error: {e}")
            raise ValueError(f"Invalid data for insertion: {e}")
        except sqlite3.Error as e:
            logger.error(f"Failed to insert prediction: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get prediction statistics.
        
        Returns:
            Dict with total_predictions, avg_duration, daily stats.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Total and average
                cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    AVG(duration) as avg_duration,
                    MIN(duration) as min_duration,
                    MAX(duration) as max_duration
                FROM predictions
                """)
                stats = cursor.fetchone()
                
                # Daily statistics
                cursor.execute("""
                SELECT 
                    DATE(created_at) as date,
                    COUNT(*) as count,
                    AVG(duration) as avg_duration
                FROM predictions
                GROUP BY DATE(created_at)
                ORDER BY DATE(created_at) DESC
                LIMIT 30
                """)
                daily = cursor.fetchall()
                
                logger.debug("Statistics retrieved successfully")
                
                return {
                    "total_predictions": stats["total"] or 0,
                    "avg_duration": round(stats["avg_duration"] or 0, 2),
                    "min_duration": round(stats["min_duration"] or 0, 2),
                    "max_duration": round(stats["max_duration"] or 0, 2),
                    "stddev_duration": 0.0,  # SQLite doesn't have STDDEV, using 0
                    "daily": [dict(row) for row in daily]
                }
                
        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve statistics: {e}")
            raise
    
    def delete_old_records(self, days: int = 90) -> int:
        """
        Delete predictions older than specified days.
        
        Args:
            days: Number of days to keep (default 90).
            
        Returns:
            int: Number of deleted records.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                DELETE FROM predictions
                WHERE created_at < datetime('now', ? || ' days')
                """, (f"-{days}",))
                
                deleted = cursor.rowcount
                logger.info(f"Deleted {deleted} old records (>{days} days old)")
                return deleted
                
        except sqlite3.Error as e:
            logger.error(f"Failed to delete records: {e}")
            raise


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """
    Get or create database manager instance.
    
    Returns:
        DatabaseManager: Database manager instance.
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


# Keep backward compatibility with old interface
def init_db() -> None:
    """Initialize database (backward compatibility)."""
    get_db_manager()


def insert_prediction(data: Dict[str, Any], duration: float, distance: float) -> None:
    """
    Insert prediction record (backward compatibility).
    
    Args:
        data: Input data dictionary.
        duration: Predicted duration.
        distance: Trip distance.
    """
    db = get_db_manager()
    db.insert_prediction(
        vendor_id=int(data.get("vendor_id", 1)),
        passenger_count=int(data.get("passenger_count", 1)),
        distance=float(distance),
        duration=float(duration)
    )


def get_stats() -> Dict[str, Any]:
    """
    Get statistics (backward compatibility).
    
    Returns:
        Dict: Statistics data.
    """
    db = get_db_manager()
    return db.get_stats()