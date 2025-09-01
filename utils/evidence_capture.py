#!/usr/bin/env python3
"""
📸 EVIDENCE SCREENSHOT CAPTURE SYSTEM
Advanced screenshot and evidence capture for Twitter monitoring
Includes metadata preservation, chain of custody, and forensic verification
"""

import os
import sys
import hashlib
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from dataclasses import dataclass, asdict
import uuid
import base64

# Try to import screenshot libraries
try:
    import requests
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("⚠️ PIL not available - screenshot functionality limited")

try:
    import selenium
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    HAS_SELENIUM = True
except ImportError:
    HAS_SELENIUM = False
    print("⚠️ Selenium not available - web screenshot functionality disabled")

@dataclass
class EvidenceMetadata:
    """Metadata structure for evidence preservation"""
    evidence_id: str
    timestamp: datetime
    source_type: str  # 'twitter', 'web', 'api'
    content_hash: str
    screenshot_hash: str
    chain_of_custody: List[Dict[str, Any]]
    verification_data: Dict[str, Any]
    legal_metadata: Dict[str, Any]

@dataclass
class TwitterEvidenceData:
    """Twitter-specific evidence data"""
    tweet_id: str
    tweet_url: str
    author_id: str
    author_username: str
    author_display_name: str
    tweet_text: str
    created_at: datetime
    metrics: Dict[str, int]
    location_data: Optional[Dict[str, Any]]
    media_urls: List[str]
    threat_assessment: Dict[str, Any]

class EvidenceCaptureSystem:
    """
    📸 Comprehensive evidence capture system
    Handles screenshot capture, metadata preservation, and chain of custody
    """
    
    def __init__(self, evidence_dir: str = "evidence/screenshots"):
        """Initialize evidence capture system"""
        self.evidence_dir = Path(evidence_dir)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger = self._setup_logging()
        self.webdriver = None
        
        # Evidence tracking
        self.evidence_index = self._load_evidence_index()
        
        print(f"📸 Evidence Capture System initialized")
        print(f"   📁 Evidence Directory: {self.evidence_dir}")
        print(f"   🔧 PIL Available: {HAS_PIL}")
        print(f"   🌐 Selenium Available: {HAS_SELENIUM}")
        print(f"   📋 Existing Evidence Items: {len(self.evidence_index)}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for evidence capture"""
        logger = logging.getLogger("EvidenceCapture")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(log_dir / "evidence_capture.log")
            console_handler = logging.StreamHandler()
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    
    def _load_evidence_index(self) -> Dict[str, Dict[str, Any]]:
        """Load evidence index from file"""
        index_file = self.evidence_dir / "evidence_index.json"
        
        try:
            if index_file.exists():
                with open(index_file, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            self.logger.error(f"Error loading evidence index: {str(e)}")
            return {}
    
    def _save_evidence_index(self):
        """Save evidence index to file"""
        index_file = self.evidence_dir / "evidence_index.json"
        
        try:
            with open(index_file, 'w') as f:
                json.dump(self.evidence_index, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Error saving evidence index: {str(e)}")
    
    def _generate_evidence_id(self) -> str:
        """Generate unique evidence ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_id = str(uuid.uuid4())[:8]
        return f"EVD_{timestamp}_{random_id}"
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {str(e)}")
            return ""
    
    def _init_webdriver(self) -> bool:
        """Initialize Chrome webdriver for screenshots"""
        if not HAS_SELENIUM:
            return False
        
        try:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            self.webdriver = webdriver.Chrome(options=chrome_options)
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing webdriver: {str(e)}")
            return False
    
    def capture_twitter_evidence(self, 
                                tweet_data: Dict[str, Any], 
                                threat_assessment: Dict[str, Any]) -> Optional[str]:
        """
        📱 Capture comprehensive evidence for Twitter content
        """
        try:
            evidence_id = self._generate_evidence_id()
            timestamp = datetime.now()
            
            # Extract Twitter data
            tweet = tweet_data.get('data', {})
            includes = tweet_data.get('includes', {})
            users = includes.get('users', [])
            user = users[0] if users else {}
            
            # Create Twitter evidence data
            twitter_evidence = TwitterEvidenceData(
                tweet_id=tweet.get('id', ''),
                tweet_url=f"https://twitter.com/i/status/{tweet.get('id', '')}",
                author_id=tweet.get('author_id', ''),
                author_username=user.get('username', ''),
                author_display_name=user.get('name', ''),
                tweet_text=tweet.get('text', ''),
                created_at=datetime.fromisoformat(tweet.get('created_at', timestamp.isoformat()).replace('Z', '+00:00')),
                metrics=tweet.get('public_metrics', {}),
                location_data=tweet.get('geo'),
                media_urls=[],  # Would be populated from media data
                threat_assessment=threat_assessment
            )
            
            # Create evidence directory for this item
            evidence_subdir = self.evidence_dir / evidence_id
            evidence_subdir.mkdir(exist_ok=True)
            
            # Save raw tweet data
            raw_data_file = evidence_subdir / "raw_tweet_data.json"
            with open(raw_data_file, 'w') as f:
                json.dump(tweet_data, f, indent=2, default=str)
            
            # Calculate content hash
            content_hash = hashlib.sha256(
                json.dumps(tweet_data, sort_keys=True, default=str).encode()
            ).hexdigest()
            
            # Capture screenshot if possible
            screenshot_file = None
            screenshot_hash = ""
            
            if twitter_evidence.tweet_url:
                screenshot_file = self._capture_web_screenshot(
                    twitter_evidence.tweet_url,
                    evidence_subdir / "tweet_screenshot.png"
                )
                if screenshot_file:
                    screenshot_hash = self._calculate_file_hash(screenshot_file)
            
            # Generate evidence summary image
            summary_image = self._create_evidence_summary_image(
                twitter_evidence,
                evidence_subdir / "evidence_summary.png"
            )
            
            # Create chain of custody
            chain_of_custody = [{
                "action": "evidence_captured",
                "timestamp": timestamp.isoformat(),
                "operator": "Twitter_Monitor_System",
                "details": "Automated evidence capture from Twitter stream",
                "system_info": {
                    "hostname": os.uname().nodename if hasattr(os, 'uname') else 'unknown',
                    "python_version": sys.version,
                    "capture_method": "api_stream"
                }
            }]
            
            # Create verification data
            verification_data = {
                "api_response_hash": content_hash,
                "screenshot_hash": screenshot_hash,
                "capture_timestamp": timestamp.isoformat(),
                "verification_signature": self._generate_verification_signature(content_hash, timestamp),
                "system_state": {
                    "disk_space": self._get_disk_space(),
                    "memory_usage": self._get_memory_usage()
                }
            }
            
            # Legal metadata
            legal_metadata = {
                "jurisdiction": "India",
                "evidence_type": "digital_social_media",
                "collection_authority": "Law_Enforcement_AI_Monitor",
                "retention_period_days": 2555,  # 7 years
                "privacy_compliance": "IT_Act_2000",
                "admissibility_notes": "Automated collection under IT Act 2000 Section 65B",
                "chain_of_custody_maintained": True
            }
            
            # Create evidence metadata
            metadata = EvidenceMetadata(
                evidence_id=evidence_id,
                timestamp=timestamp,
                source_type="twitter",
                content_hash=content_hash,
                screenshot_hash=screenshot_hash,
                chain_of_custody=chain_of_custody,
                verification_data=verification_data,
                legal_metadata=legal_metadata
            )
            
            # Save metadata
            metadata_file = evidence_subdir / "evidence_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(asdict(metadata), f, indent=2, default=str)
            
            # Save Twitter-specific evidence
            twitter_evidence_file = evidence_subdir / "twitter_evidence.json"
            with open(twitter_evidence_file, 'w') as f:
                json.dump(asdict(twitter_evidence), f, indent=2, default=str)
            
            # Update evidence index
            self.evidence_index[evidence_id] = {
                "evidence_id": evidence_id,
                "timestamp": timestamp.isoformat(),
                "source_type": "twitter",
                "tweet_id": twitter_evidence.tweet_id,
                "author_username": twitter_evidence.author_username,
                "threat_level": threat_assessment.get('threat_level', 'UNKNOWN'),
                "content_hash": content_hash,
                "files": {
                    "metadata": str(metadata_file.relative_to(self.evidence_dir)),
                    "raw_data": str(raw_data_file.relative_to(self.evidence_dir)),
                    "twitter_evidence": str(twitter_evidence_file.relative_to(self.evidence_dir)),
                    "screenshot": str(screenshot_file.relative_to(self.evidence_dir)) if screenshot_file else None,
                    "summary_image": str(summary_image.relative_to(self.evidence_dir)) if summary_image else None
                }
            }
            
            self._save_evidence_index()
            
            self.logger.info(f"Evidence captured successfully: {evidence_id}")
            print(f"📸 Evidence captured: {evidence_id}")
            print(f"   🐦 Tweet ID: {twitter_evidence.tweet_id}")
            print(f"   👤 Author: @{twitter_evidence.author_username}")
            print(f"   🚨 Threat Level: {threat_assessment.get('threat_level', 'UNKNOWN')}")
            
            return evidence_id
            
        except Exception as e:
            self.logger.error(f"Error capturing Twitter evidence: {str(e)}")
            return None
    
    def _capture_web_screenshot(self, url: str, output_path: Path) -> Optional[Path]:
        """Capture screenshot of web page"""
        if not HAS_SELENIUM:
            return None
        
        try:
            if not self.webdriver:
                if not self._init_webdriver():
                    return None
            
            self.webdriver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Take screenshot
            self.webdriver.save_screenshot(str(output_path))
            
            self.logger.info(f"Screenshot captured: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error capturing screenshot: {str(e)}")
            return None
    
    def _create_evidence_summary_image(self, 
                                     twitter_evidence: TwitterEvidenceData,
                                     output_path: Path) -> Optional[Path]:
        """Create evidence summary image with key information"""
        if not HAS_PIL:
            return None
        
        try:
            # Create image
            width, height = 800, 600
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to load font (fallback to default if not available)
            try:
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
            
            # Draw header
            draw.rectangle([0, 0, width, 60], fill='#1DA1F2')
            draw.text((20, 20), "🐦 TWITTER EVIDENCE CAPTURE", fill='white', font=title_font)
            
            # Draw evidence details
            y_pos = 80
            line_height = 25
            
            details = [
                f"Evidence ID: {twitter_evidence.tweet_id}",
                f"Tweet ID: {twitter_evidence.tweet_id}",
                f"Author: @{twitter_evidence.author_username} ({twitter_evidence.author_display_name})",
                f"Created: {twitter_evidence.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
                f"Captured: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
                "",
                "Tweet Content:",
                twitter_evidence.tweet_text[:200] + ("..." if len(twitter_evidence.tweet_text) > 200 else ""),
                "",
                f"Metrics: {twitter_evidence.metrics}",
                f"Threat Assessment: {twitter_evidence.threat_assessment}",
                "",
                "⚖️ This evidence was captured automatically by the Police AI Monitor system",
                "📋 Chain of custody and verification data preserved in metadata files",
                "🔐 Hash verification ensures evidence integrity"
            ]
            
            for detail in details:
                if detail:  # Skip empty lines
                    draw.text((20, y_pos), detail, fill='black', font=text_font)
                y_pos += line_height
                if y_pos > height - 40:
                    break
            
            # Draw footer
            draw.rectangle([0, height-40, width, height], fill='#E1E8ED')
            draw.text((20, height-30), f"Generated by Police AI Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                     fill='black', font=text_font)
            
            # Save image
            img.save(output_path)
            
            self.logger.info(f"Evidence summary image created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating evidence summary image: {str(e)}")
            return None
    
    def _generate_verification_signature(self, content_hash: str, timestamp: datetime) -> str:
        """Generate verification signature for evidence integrity"""
        signature_data = f"{content_hash}:{timestamp.isoformat()}:police_ai_monitor"
        return hashlib.sha256(signature_data.encode()).hexdigest()
    
    def _get_disk_space(self) -> Dict[str, int]:
        """Get current disk space information"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.evidence_dir)
            return {
                "total_bytes": total,
                "used_bytes": used,
                "free_bytes": free
            }
        except:
            return {}
    
    def _get_memory_usage(self) -> Dict[str, int]:
        """Get current memory usage information"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                "total_bytes": memory.total,
                "available_bytes": memory.available,
                "used_bytes": memory.used,
                "percent_used": memory.percent
            }
        except:
            return {}
    
    def verify_evidence_integrity(self, evidence_id: str) -> Dict[str, bool]:
        """
        🔍 Verify evidence integrity using hashes and signatures
        """
        try:
            if evidence_id not in self.evidence_index:
                return {"error": "Evidence not found"}
            
            evidence_info = self.evidence_index[evidence_id]
            evidence_subdir = self.evidence_dir / evidence_id
            
            if not evidence_subdir.exists():
                return {"error": "Evidence directory not found"}
            
            verification_results = {}
            
            # Verify metadata file
            metadata_file = evidence_subdir / "evidence_metadata.json"
            if metadata_file.exists():
                verification_results["metadata_file"] = True
                
                # Load and verify metadata
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                # Verify content hash
                raw_data_file = evidence_subdir / "raw_tweet_data.json"
                if raw_data_file.exists():
                    with open(raw_data_file, 'r') as f:
                        raw_data = json.load(f)
                    
                    calculated_hash = hashlib.sha256(
                        json.dumps(raw_data, sort_keys=True, default=str).encode()
                    ).hexdigest()
                    
                    verification_results["content_hash"] = (
                        calculated_hash == metadata.get("content_hash", "")
                    )
                else:
                    verification_results["content_hash"] = False
                
                # Verify screenshot hash if exists
                screenshot_file = evidence_subdir / "tweet_screenshot.png"
                if screenshot_file.exists():
                    screenshot_hash = self._calculate_file_hash(screenshot_file)
                    verification_results["screenshot_hash"] = (
                        screenshot_hash == metadata.get("screenshot_hash", "")
                    )
                else:
                    verification_results["screenshot_hash"] = True  # No screenshot to verify
                
                # Verify signature
                content_hash = metadata.get("content_hash", "")
                timestamp_str = metadata.get("verification_data", {}).get("capture_timestamp", "")
                expected_signature = self._generate_verification_signature(
                    content_hash, 
                    datetime.fromisoformat(timestamp_str)
                )
                actual_signature = metadata.get("verification_data", {}).get("verification_signature", "")
                verification_results["verification_signature"] = (expected_signature == actual_signature)
                
            else:
                verification_results["metadata_file"] = False
            
            return verification_results
            
        except Exception as e:
            self.logger.error(f"Error verifying evidence integrity: {str(e)}")
            return {"error": str(e)}
    
    def get_evidence_summary(self) -> Dict[str, Any]:
        """
        📊 Get summary of all captured evidence
        """
        try:
            total_evidence = len(self.evidence_index)
            
            # Count by source type
            source_counts = {}
            threat_counts = {}
            monthly_counts = {}
            
            for evidence_id, info in self.evidence_index.items():
                # Source type
                source_type = info.get("source_type", "unknown")
                source_counts[source_type] = source_counts.get(source_type, 0) + 1
                
                # Threat level
                threat_level = info.get("threat_level", "unknown")
                threat_counts[threat_level] = threat_counts.get(threat_level, 0) + 1
                
                # Monthly distribution
                timestamp = info.get("timestamp", "")
                if timestamp:
                    try:
                        month_key = datetime.fromisoformat(timestamp).strftime("%Y-%m")
                        monthly_counts[month_key] = monthly_counts.get(month_key, 0) + 1
                    except:
                        pass
            
            # Calculate storage usage
            storage_usage = 0
            for evidence_subdir in self.evidence_dir.iterdir():
                if evidence_subdir.is_dir() and evidence_subdir.name.startswith("EVD_"):
                    for file_path in evidence_subdir.rglob("*"):
                        if file_path.is_file():
                            storage_usage += file_path.stat().st_size
            
            return {
                "total_evidence_items": total_evidence,
                "source_distribution": source_counts,
                "threat_distribution": threat_counts,
                "monthly_distribution": monthly_counts,
                "storage_usage_bytes": storage_usage,
                "storage_usage_mb": round(storage_usage / (1024 * 1024), 2),
                "evidence_directory": str(self.evidence_dir),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting evidence summary: {str(e)}")
            return {"error": str(e)}
    
    def cleanup_old_evidence(self, retention_days: int = 90) -> Dict[str, int]:
        """
        🧹 Clean up evidence older than retention period
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            items_removed = 0
            bytes_freed = 0
            
            evidence_to_remove = []
            
            for evidence_id, info in self.evidence_index.items():
                timestamp_str = info.get("timestamp", "")
                if timestamp_str:
                    try:
                        evidence_date = datetime.fromisoformat(timestamp_str)
                        if evidence_date < cutoff_date:
                            evidence_to_remove.append(evidence_id)
                    except:
                        continue
            
            # Remove old evidence
            for evidence_id in evidence_to_remove:
                evidence_subdir = self.evidence_dir / evidence_id
                if evidence_subdir.exists():
                    # Calculate size before removal
                    for file_path in evidence_subdir.rglob("*"):
                        if file_path.is_file():
                            bytes_freed += file_path.stat().st_size
                    
                    # Remove directory
                    import shutil
                    shutil.rmtree(evidence_subdir)
                    items_removed += 1
                
                # Remove from index
                del self.evidence_index[evidence_id]
            
            # Save updated index
            self._save_evidence_index()
            
            self.logger.info(f"Cleaned up {items_removed} evidence items, freed {bytes_freed} bytes")
            
            return {
                "items_removed": items_removed,
                "bytes_freed": bytes_freed,
                "retention_days": retention_days,
                "cutoff_date": cutoff_date.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error cleaning up evidence: {str(e)}")
            return {"error": str(e)}
    
    def close(self):
        """Close webdriver and cleanup resources"""
        if self.webdriver:
            try:
                self.webdriver.quit()
            except:
                pass
            self.webdriver = None


def test_evidence_capture():
    """Test evidence capture system"""
    print("\n🧪 TESTING EVIDENCE CAPTURE SYSTEM")
    print("=" * 80)
    
    # Test 1: Initialize system
    print("\n1️⃣ Testing System Initialization...")
    capture_system = EvidenceCaptureSystem("test_evidence")
    init_success = capture_system.evidence_dir.exists()
    print(f"   Status: {'✅ INITIALIZED' if init_success else '❌ FAILED'}")
    
    # Test 2: Create mock Twitter evidence
    print("\n2️⃣ Testing Twitter Evidence Capture...")
    mock_tweet_data = {
        "data": {
            "id": "1234567890123456789",
            "text": "Test tweet for evidence capture system demonstration",
            "author_id": "987654321",
            "created_at": "2025-09-01T12:00:00.000Z",
            "public_metrics": {
                "retweet_count": 5,
                "like_count": 15,
                "reply_count": 3,
                "quote_count": 1
            }
        },
        "includes": {
            "users": [{
                "id": "987654321",
                "username": "test_user",
                "name": "Test User"
            }]
        }
    }
    
    mock_threat_assessment = {
        "threat_level": "HIGH",
        "sentiment_score": -0.8,
        "bot_probability": 0.2
    }
    
    evidence_id = capture_system.capture_twitter_evidence(mock_tweet_data, mock_threat_assessment)
    capture_success = evidence_id is not None
    print(f"   Status: {'✅ CAPTURED' if capture_success else '❌ FAILED'}")
    if evidence_id:
        print(f"      📋 Evidence ID: {evidence_id}")
    
    # Test 3: Verify evidence integrity
    print("\n3️⃣ Testing Evidence Verification...")
    if evidence_id:
        verification_results = capture_system.verify_evidence_integrity(evidence_id)
        verification_success = not verification_results.get("error") and verification_results.get("content_hash", False)
        print(f"   Status: {'✅ VERIFIED' if verification_success else '❌ FAILED'}")
        if verification_results:
            for check, result in verification_results.items():
                if check != "error":
                    status = "✅" if result else "❌"
                    print(f"      {status} {check}")
    else:
        verification_success = False
        print("   Status: ❌ SKIPPED (no evidence to verify)")
    
    # Test 4: Evidence summary
    print("\n4️⃣ Testing Evidence Summary...")
    summary = capture_system.get_evidence_summary()
    summary_success = not summary.get("error") and summary.get("total_evidence_items", 0) > 0
    print(f"   Status: {'✅ GENERATED' if summary_success else '❌ FAILED'}")
    if summary_success:
        print(f"      📊 Total Items: {summary['total_evidence_items']}")
        print(f"      💾 Storage: {summary['storage_usage_mb']} MB")
    
    # Test 5: Cleanup
    print("\n5️⃣ Testing Cleanup...")
    cleanup_results = capture_system.cleanup_old_evidence(retention_days=0)  # Clean everything for test
    cleanup_success = not cleanup_results.get("error")
    print(f"   Status: {'✅ CLEANED' if cleanup_success else '❌ FAILED'}")
    
    # Close system
    capture_system.close()
    
    # Remove test directory
    try:
        import shutil
        shutil.rmtree("test_evidence")
        print("   🧹 Test files cleaned up")
    except:
        pass
    
    # Summary
    print(f"\n📊 EVIDENCE CAPTURE TEST SUMMARY")
    print("=" * 80)
    
    results = [
        ('System Initialization', init_success),
        ('Twitter Evidence Capture', capture_success),
        ('Evidence Verification', verification_success),
        ('Evidence Summary', summary_success),
        ('Cleanup Function', cleanup_success)
    ]
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Overall Success Rate: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("🏆 EVIDENCE CAPTURE SYSTEM FULLY OPERATIONAL!")
    elif passed_tests >= total_tests * 0.8:
        print("🥇 EVIDENCE CAPTURE SYSTEM WORKING WELL!")
    else:
        print("⚠️ EVIDENCE CAPTURE SYSTEM NEEDS ATTENTION")
    
    return {
        'total_tests': total_tests,
        'passed_tests': passed_tests,
        'success_rate': passed_tests / total_tests,
        'results': dict(results)
    }


if __name__ == "__main__":
    test_evidence_capture()
